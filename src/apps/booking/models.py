import datetime

from django.contrib.auth.models import User
from django.db import models

from common.models import BaseModel, tomorrow_date


class Room(BaseModel):
    title = models.CharField("Title", max_length=120)
    daily_cost = models.DecimalField("Daily cost", max_digits=16, decimal_places=4)
    place_count = models.PositiveIntegerField("Place count")

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    def __str__(self) -> str:
        return f"Room - {self.title}"


class Booking(BaseModel):
    start = models.DateTimeField("Start", default=datetime.datetime.now)
    finish = models.DateTimeField("Finish", default=tomorrow_date)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Rooms")
    person = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Booked by")

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        constraints = [
            models.CheckConstraint(
                check=(models.Q(finish__gt=models.F("start"))),
                name="check_finish",
                violation_error_message="Booking finish cant be before booking start.",
            )
        ]

    def __str__(self) -> str:
        return f"Booking [{self.room}] by {self.person.username}"
