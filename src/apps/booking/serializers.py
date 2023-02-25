from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Booking, Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    person = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"

    def create(self, validated_data: dict) -> Booking:
        if validated_data["start"] > validated_data["finish"]:
            raise ValidationError("Booking start date can't be later than booking finish date")
        if Booking.objects.filter(
            start__lte=validated_data["start"], finish__gte=validated_data["start"], room=validated_data["room"]
        ).exists():
            raise ValidationError("Room is booked")
        validated_data["person"] = self.context.get("request").user

        return super().create(validated_data)
