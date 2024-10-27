from datetime import datetime, date

from django.urls import reverse
from rest_framework.test import APITestCase

import pytz
import requests
import random

utc = pytz.timezone("UTC")

BASE_URL = "http://provider:8000"


class EventsViewSetTestCase(APITestCase):

    def test_get_events_list(self):
        url = f"{BASE_URL}{reverse("events-list")}"
        date_format = "%Y-%m-%d"
        params = {
            "updated__gte": utc.localize(datetime.strptime("2022-01-01", date_format)),
            "updated__lte": utc.localize(datetime.strptime("2022-02-01", date_format)),
        }
        response = requests.get(url, params)
        print(response.json())
        self.assertEqual(response.status_code, 200)

    def test_get_events_with_hotel_id_A(self):
        url = f"{BASE_URL}{reverse("events-list")}"
        params = {"hotel_id": "3539"}
        response = requests.get(url, params)
        print(response.json())
        self.assertEqual(response.status_code, 200)

    def test_get_events_with_hotel_id_B(self):
        url = f"{BASE_URL}{reverse("events-list")}"
        params = {"hotel_id": "2607"}
        response = requests.get(url, params)
        print(response.json())
        self.assertEqual(response.status_code, 200)

    def test_get_events_with_hotel_id_C(self):
        url = f"{BASE_URL}{reverse("events-list")}"
        params = {"hotel_id": "3009"}
        response = requests.get(url, params)
        print(response.json())
        self.assertEqual(response.status_code, 200)

    def test_create_new_event(self):
        data = {
            "hotel_id": random.choice([2607, 3539, 3009]),
            "rpg_status": random.choice([1, 2]),
            "room_id": random.randrange(start=19000000, stop=19999999),
            "night_of_stay": date.today(),
            "timestamp": datetime.now().isoformat(),
        }
        url = f"{BASE_URL}{reverse("events-list")}"
        response = requests.post(url, data)
        print(response.json())
        self.assertEqual(response.status_code, 201)
