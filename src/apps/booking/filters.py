from django_filters import rest_framework as filters

from .models import Booking, Room


class RoomFilter(filters.FilterSet):
    """Room filters class"""

    cost__gt = filters.NumberFilter(field_name="daily_cost", lookup_expr="gt")
    cost__lt = filters.NumberFilter(field_name="daily_cost", lookup_expr="lt")

    class Meta:
        model = Room
        fields = ("daily_cost", "place_count")


class UnbookedFilter(filters.FilterSet):
    """Unbooked rooms filters class"""

    start = filters.DateTimeFilter(field_name="start", lookup_expr="gte")
    finish = filters.DateTimeFilter(field_name="finish", lookup_expr="lte")

    class Meta:
        model = Booking
        fields = ("start", "finish")
