from django_filters import rest_framework as filters

from .models import Room


class RoomFilter(filters.FilterSet):
    cost__gt = filters.NumberFilter(field_name="daily_cost", lookup_expr="gt")
    cost__lt = filters.NumberFilter(field_name="daily_cost", lookup_expr="lt")

    class Meta:
        model = Room
        fields = ("daily_cost", "place_count")


class UnbookedFilter(filters.FilterSet):
    start = filters.DateTimeFilter(field_name="start", lookup_expr="gte")
    finish = filters.DateTimeFilter(field_name="finish", lookup_expr="lte")

    class Meta:
        model = Room
        fields = ("start", "finish")
