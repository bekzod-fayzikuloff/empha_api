from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .filters import RoomFilter, UnbookedFilter
from .models import Booking, Room
from .permissions import IsBookedByHimselfOrReadOnly
from .serializers import BookingSerializer, RoomSerializer


class RoomViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filterset_class = RoomFilter
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["place_count", "daily_cost", "-place_count", "-daily_cost"]


class UnbookedViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filterset_class = UnbookedFilter
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> QuerySet:
        start = self.request.query_params.get("start")
        finish = self.request.query_params.get("finish")
        if not all((start, finish)):
            raise ValidationError("Request should have start and finish query params")
        return super().get_queryset()


class BookingViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsBookedByHimselfOrReadOnly]

    def get_queryset(self) -> QuerySet:
        if self.action != "list":
            return Booking.objects.all()

        return Booking.objects.filter(person=self.request.user)
