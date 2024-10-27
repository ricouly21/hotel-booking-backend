from django.urls import reverse
from rest_framework.test import APITestCase


class DashboardViewTestCase(APITestCase):

    def test_get_daily_bookings(self):
        url = reverse("dashboard")
        params = {"period": "day", "year": "2022"}
        response = self.client.get(url, params)
        print(response.json())
        self.assertEqual(response.status_code, 200)

    def test_get_monthly_bookings(self):
        url = reverse("dashboard")
        params = {"period": "month", "year": "2022"}
        response = self.client.get(url, params)
        print(response.json())
        self.assertEqual(response.status_code, 200)
