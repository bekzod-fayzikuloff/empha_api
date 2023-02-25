from django.db.models import QuerySet
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

    @extend_schema(methods=["GET"], tags=["rooms"])
    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        Rooms list endpoint handling view.
        Parameters
        ----------
        request : Request
            rest_framework.request.Request - `django.http.request.HttpRequest`'s subclass
        *args : tuple
            Multiple position function argument
        **kwargs : dict
            Named function arguments
        Returns
        -------
        _ : Response
            Rooms list endpoint response with filtering and ordering support
        """
        return super().list(request, *args, **kwargs)

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
        Parameters
        ----------
        request : Request
            rest_framework.request.Request - `django.http.request.HttpRequest`'s subclass
        *args : tuple
            Multiple position function argument
        **kwargs : dict
            Named function arguments
        Returns
        -------
        _ : Response
            Unbooked rooms list endpoint response
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
        return Room.objects.exclude(booking__start__gte=start, booking__finish__lte=finish)


class BookingViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsBookedByHimselfOrReadOnly]

    @extend_schema(methods=["GET"], tags=["booking"], description="List of booked a room")
    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        Booked rooms endpoint handling view.
        Parameters
        ----------
        request : Request
            rest_framework.request.Request - `django.http.request.HttpRequest`'s subclass
        *args : tuple
            Multiple position function argument
        **kwargs : dict
            Named function arguments
        Returns
        -------
        _ : Response
            Booked rooms list endpoint response
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(methods=["POST"], tags=["booking"], description="Book a room")
    def create(self, request: Request, *args, **kwargs) -> Response:
        """
        Create book rooms endpoint handling view.
        Parameters
        ----------
        request : Request
            rest_framework.request.Request - `django.http.request.HttpRequest`'s subclass
        *args : tuple
            Multiple position function argument
        **kwargs : dict
            Named function arguments
        Returns
        -------
        _ : Response
            Booked room endpoint response
        """
        return super().create(request, *args, **kwargs)

    @extend_schema(methods=["DELETE"], tags=["booking"], description="Cancel your booking")
    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """
        Cancel your booking endpoint handling view.
        Parameters
        ----------
        request : Request
            rest_framework.request.Request - `django.http.request.HttpRequest`'s subclass
        *args : tuple
            Multiple position function argument
        **kwargs : dict
            Named function arguments
        Returns
        -------
        _ : Response
            204 status
        """
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet:
        if self.action != "list":
            return Booking.objects.all()

        return Booking.objects.filter(person=self.request.user)
