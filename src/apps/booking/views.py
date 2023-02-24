from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from .filters import RoomFilter
from .models import Booking, Room
from .serializers import BookingSerializer, RoomSerializer


class RoomViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filterset_class = RoomFilter

    @extend_schema(
        methods=["GET"],
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
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


class BookingViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
