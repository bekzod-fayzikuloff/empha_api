import datetime
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


class UnbookedAPITestCase(APITestCase):
    def setUp(self) -> None:
        for pk, cost, count in [(1, 2000.0, 2), (2, 2500.0, 3), (3, 2700.0, 3)]:
            Room.objects.create(title=f"Room #{pk}", daily_cost=Decimal(cost), place_count=count)

    def test_unbooked_without_timerange(self):
        response = self.client.get("/api/rooms/unbooked/", format="json")

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue("Request should have start and finish query params" in response.json())

    def test_unbooked_with_timerange_no_exist_bookings(self):
        start = datetime.date.today()
        start_str = start.strftime("%Y-%m-%d")
        finish_str = (start + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        response = self.client.get(f"/api/rooms/unbooked/?finish={finish_str}&start={start_str}", format="json")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(len(response.json()), Room.objects.count())
