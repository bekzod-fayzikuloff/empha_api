from django.contrib import admin

from .models import Booking, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_filter = ("place_count",)
    search_fields = ("title", "daily_cost")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    search_fields = ("room__title", "person__username")
    list_filter = ("room__place_count",)
