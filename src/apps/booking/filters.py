from django_filters import rest_framework as filters

from .models import Room


class RoomFilter(filters.FilterSet):
    cost__gt = filters.NumberFilter(field_name="daily_cost", lookup_expr="gt")
    cost__lt = filters.NumberFilter(field_name="daily_cost", lookup_expr="lt")

    class Meta:
        model = Room
        fields = ("daily_cost", "place_count")


class UnbookedFilter(filters.FilterSet):
    start = filters.DateTimeFilter(field_name="booking__start", lookup_expr="lte", exclude=True)
    finish = filters.DateTimeFilter(field_name="booking__finish", lookup_expr="lte", exclude=True)

    class Meta:
        model = Room
        fields = ("start", "finish")
