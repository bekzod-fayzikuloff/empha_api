from django.db.models import Q, QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from common.utils import parse_datetime_qs

from .filters import RoomFilter, UnbookedFilter
from .models import Booking, Room
from .permissions import IsBookedByHimselfOrReadOnly
from .serializers import BookingSerializer, RoomSerializer


class RoomViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filterset_class = RoomFilter
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        order = self.request.query_params.get("orderBy")
        if order is not None:
            match order:
                case "count":
                    queryset = queryset.order_by("place_count")
                case "countDesc":
                    queryset = queryset.order_by("-place_count")
                case "cost":
                    queryset = queryset.order_by("daily_cost")
                case "costDesc":
                    queryset = queryset.order_by("-daily_cost")
                case _:
                    return queryset
        return queryset


class UnbookedViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filterset_class = UnbookedFilter
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(methods=["GET"], tags=["rooms"])
    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        Unbooked rooms endpoint handling view.
        """
        queryset: QuerySet = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self) -> QuerySet:
        start = self.request.query_params.get("start")
        finish = self.request.query_params.get("finish")
        if not all((start, finish)):
            raise ValidationError("Request should have start and finish query params")
        start = parse_datetime_qs(start)
        finish = parse_datetime_qs(finish)
        return Room.objects.exclude(Q(booking__start__lte=start) & Q(booking__finish__lte=finish))


class BookingViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsBookedByHimselfOrReadOnly]

    def get_queryset(self) -> QuerySet:
        if self.action != "list":
            return Booking.objects.all()

        return Booking.objects.filter(person=self.request.user)
