from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Room
from .serializers import RoomSerializer


class RoomsAPITestCase(APITestCase):
    def setUp(self) -> None:
        Room.objects.create(title="Room #1", daily_cost=Decimal(2000.0), place_count=2)
        Room.objects.create(title="Room #2", daily_cost=Decimal(2500.0), place_count=3)

    def test_room_endpoint(self):
        rooms_res = self.client.get("/api/rooms/", format="json")

        self.assertEqual(status.HTTP_200_OK, rooms_res.status_code)
        self.assertEqual(len(rooms_res.json()), 2)

    def test_room_endpoint_add(self):
        Room.objects.create(title="Room #3", daily_cost=Decimal(1500.0), place_count=2)
        rooms_res = self.client.get("/api/rooms/", format="json")

        self.assertEqual(status.HTTP_200_OK, rooms_res.status_code)
        self.assertEqual(len(rooms_res.json()), 3)

    def test_room_endpoint_filter_by_count(self):
        filter_count = 2
        Room.objects.create(title="Room #3", daily_cost=Decimal(1500.0), place_count=2)

        filtered_rooms = Room.objects.filter(place_count=filter_count).count()

        rooms_res = self.client.get(f"/api/rooms/?place_count={filter_count}", format="json")

        self.assertEqual(status.HTTP_200_OK, rooms_res.status_code)
        self.assertEqual(len(rooms_res.json()), filtered_rooms)

    def test_room_order_by_cost_asc(self):
        serialized_rooms = [dict(room) for room in RoomSerializer(Room.objects.order_by("daily_cost"), many=True).data]

        rooms_res = self.client.get(f"/api/rooms/?orderBy=cost", format="json")

        self.assertEqual(status.HTTP_200_OK, rooms_res.status_code)
        self.assertEqual(rooms_res.json(), serialized_rooms)

    def test_room_order_by_cost_desc(self):
        serialized_rooms = [dict(room) for room in RoomSerializer(Room.objects.order_by("-daily_cost"), many=True).data]

        rooms_res = self.client.get(f"/api/rooms/?orderBy=costDesc", format="json")

        self.assertEqual(status.HTTP_200_OK, rooms_res.status_code)
        self.assertEqual(rooms_res.json(), serialized_rooms)

    def test_room_order_by_count_asc(self):
        serialized_rooms = [dict(room) for room in RoomSerializer(Room.objects.order_by("place_count"), many=True).data]
        rooms_res = self.client.get(f"/api/rooms/?orderBy=count", format="json")

        rooms_res_json = rooms_res.json()

        self.assertEqual(status.HTTP_200_OK, rooms_res.status_code)
        self.assertEqual(rooms_res_json, serialized_rooms)

        self.assertTrue(rooms_res_json[0]["place_count"] < rooms_res_json[1]["place_count"])

    def test_room_order_by_count_desc(self):
        serialized_rooms = [
            dict(room) for room in RoomSerializer(Room.objects.order_by("-place_count"), many=True).data
        ]
        rooms_res = self.client.get(f"/api/rooms/?orderBy=countDesc", format="json")
        rooms_res_json = rooms_res.json()

        self.assertEqual(status.HTTP_200_OK, rooms_res.status_code)
        self.assertEqual(rooms_res_json, serialized_rooms)
        self.assertTrue(rooms_res_json[0]["place_count"] > rooms_res_json[1]["place_count"])

    def test_filtering_by_cost(self):
        Room.objects.create(title="Room #3", daily_cost=Decimal(1500.0), place_count=2)
        rooms_res = self.client.get(f"/api/rooms/?cost__lt=2200&" f"cost__gt=1400", format="json")

        rooms_res_json = rooms_res.json()

        self.assertEqual(status.HTTP_200_OK, rooms_res.status_code)
        self.assertEqual(len(rooms_res_json), 2)
