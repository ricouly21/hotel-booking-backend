import requests
import os
import pytz
import time

from datetime import datetime
from dateutil.relativedelta import relativedelta

from rest_framework.views import APIView

from django.views import View
from django.shortcuts import redirect
from django.http.response import JsonResponse

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


utc = pytz.timezone("UTC")

API_URL = os.getenv("API_URL", "/events")

MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def index(request):
    return redirect("dashboard")


class DashboardView(APIView):

    def sanitize_query_params(self, query_params):
        params = dict()
        for key in query_params:
            if query_params.get(key):
                params[str(key)] = query_params.get(key)
        return params

    def get_monthly_bookings(self, year: int, params: dict):
        json_data = dict()
        for i in range(0, 12):
            current_month = utc.localize(datetime(year, i + 1, 1))
            next_month = current_month + relativedelta(months=1)
            params["timestamp__gte"] = current_month
            params["timestamp__lte"] = next_month

            route = requests.get(API_URL, params=params)
            json_data[f"{MONTHS[i]}-{year}"] = {
                "number_of_bookings": len(route.json()),
            }

        return json_data

    def get_daily_bookings(self, year: int, params: dict):
        json_data = dict()
        current_date = utc.localize(datetime(int(year), 1, 1))
        while current_date.year == int(year):
            next_date = current_date + relativedelta(days=1)
            params["timestamp__gte"] = current_date.strftime("%Y-%m-%d")
            params["timestamp__lte"] = next_date.strftime("%Y-%m-%d")

            route = requests.get(API_URL, params=params)
            json_data[f"{current_date.strftime("%Y-%m-%d")}"] = {
                "number_of_bookings": len(route.json())
            }
            current_date = next_date
        return json_data

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "hotel_id",
                openapi.IN_QUERY,
                description="The ID of the hotel (optional)",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
            openapi.Parameter(
                "period",
                openapi.IN_QUERY,
                description="`day` to retrieve the daily number of bookings; `month` to retrieve the monthly number of bookings (optional).",
                type=openapi.TYPE_STRING,
                required=False,
                default="month",
            ),
            openapi.Parameter(
                "year",
                openapi.IN_QUERY,
                description="The year on where to retrieve the number of bookings.",
                type=openapi.TYPE_STRING,
                required=False,
                default="2022",
            ),
        ]
    )
    def get(self, request):
        """
        Retrieves provides the following information:

        - The monthly number of bookings for a particular hotel for the year of choice;
        - or the daily number of bookings for a particular hotel for the year of choice

        ## Query Parameters:
        - `hotel_id`: <int> The ID of the hotel (optional).
        - `period`: <str> `day` to retrieve the daily number of bookings; `month` to retrieve the monthly number of bookings (optional).
        - `year`: <str> The year on where to retrieve the number of bookings.
        """
        start_time = time.perf_counter()
        params = self.sanitize_query_params(request.GET)
        json_data = dict()

        year = params.get("year", datetime.now().strftime("%Y"))
        period = params.get("period")

        _params = {**params}
        if "period" in _params:
            _params.pop("period")
        if "year" in _params:
            _params.pop("year")

        if period == "month":
            json_data = self.get_monthly_bookings(int(year), _params)
        elif period == "day":
            json_data = self.get_daily_bookings(int(year), _params)
        else:
            current_date = utc.localize(
                datetime.strptime(
                    params.get(
                        "timestamp__gte", f"{datetime.now().strftime("%Y-%m-%d")}"
                    ),
                    "%Y-%m-%d",
                )
            )
            max_date = utc.localize(
                datetime.strptime(
                    params.get(
                        "timestamp__lte", f"{datetime.now().strftime("%Y-%m-%d")}"
                    ),
                    "%Y-%m-%d",
                )
            )
            while current_date < max_date:
                next_date = current_date + relativedelta(days=1)
                params["timestamp__gte"] = current_date.strftime("%Y-%m-%d")
                params["timestamp__lte"] = next_date.strftime("%Y-%m-%d")
                route = requests.get(API_URL, params=params)
                json_data[f"{current_date.strftime("%Y-%m-%d")}"] = {
                    "number_of_bookings": len(route.json())
                }
                current_date = next_date

        print(f"Done in {time.perf_counter() - start_time} second(s)")
        return JsonResponse(json_data, safe=False)
