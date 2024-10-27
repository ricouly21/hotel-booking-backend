from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Event


class EventsSerializer(serializers.ModelSerializer):
    night_of_stay = serializers.SerializerMethodField(method_name="_night_of_stay")

    def _night_of_stay(self, instance):
        return f"{instance.night_of_stay.strftime(format="%Y-%m-%d")}"

    class Meta:
        model = Event
        fields = [
            "id",
            "hotel_id",
            "timestamp",
            "rpg_status",
            "room_id",
            "night_of_stay",
        ]


class CreateEventSerializer(serializers.Serializer):
    hotel_id = serializers.IntegerField()
    timestamp = serializers.DateTimeField()
    rpg_status = serializers.ChoiceField(choices=["1", "2"])
    room_id = serializers.IntegerField()
    night_of_stay = serializers.DateField()

    def create(self, validated_data):
        return Event.objects.create(
            hotel_id=validated_data["hotel_id"],
            event_timestamp=validated_data["timestamp"],
            rpg_status=validated_data["rpg_status"],
            room_id=validated_data["room_id"],
            night_of_stay=validated_data["night_of_stay"],
        )


class EventsViewset(viewsets.ViewSet):

    def sanitize_query_params(self, query_params):
        params = dict()
        for key in query_params:
            _key = key
            if "id" in key and "hotel_id" not in key:
                s = key.split("__")
                s[0] = "event_id"
                _key = "__".join(s)
            if "timestamp" in key:
                s = key.split("__")
                s[0] = "event_timestamp"
                _key = "__".join(s)
            if "updated" in key:
                _key = key.replace("updated", "event_timestamp")
            if query_params.get(key):
                params[str(_key)] = query_params.get(key)
        return params

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "hotel_id",
                openapi.IN_QUERY,
                description="The ID of the hotel (optional)",
                type=openapi.TYPE_INTEGER,
                required=False,
                default="2607",
            ),
            openapi.Parameter(
                "timestamp__gte",
                openapi.IN_QUERY,
                description="`day` to retrieve the daily number of bookings; `month` to retrieve the monthly number of bookings (optional).",
                type=openapi.TYPE_STRING,
                required=False,
                default="2022-01-30",
            ),
            openapi.Parameter(
                "timestamp__lte",
                openapi.IN_QUERY,
                description="The year on where to retrieve the number of bookings.",
                type=openapi.TYPE_STRING,
                required=False,
                default="2022-02-01",
            ),
            openapi.Parameter(
                "rpg_status",
                openapi.IN_QUERY,
                description="`1` for bookings | `2` for cancellations (optional).",
                type=openapi.TYPE_STRING,
                required=False,
                default="1",
            ),
            openapi.Parameter(
                "room_id",
                openapi.IN_QUERY,
                description="The ID for the room (optional)",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                "night_of_stay",
                openapi.IN_QUERY,
                description="The date of the night of stay in the format `%Y-%m-%d` (optional).",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ]
    )
    def list(self, request):
        """
        Retrieve a list of Events.

        ## Query Parameters:
        - `hotel_id`: <int> The ID of the hotel (optional).
        - `timestamp`: <str|datetime> Timestamp of event in the format `%Y-%m-%dT%H:%M:%S` (optional).
        - `rpg_status`: <str|int> `1` for bookings | `2` for cancellations (optional).
        - `room_id`: <int> The ID for the room (optional).
        - `night_of_stay`: <str|date> The date of the night of stay in the format `%Y-%m-%d` (optional).

        ## Responses:
        - 200: Successful response.
        - 500: Error response.
        """
        params = self.sanitize_query_params(request.GET)
        try:
            queryset = Event.objects.filter(**params)
            serializer = EventsSerializer(queryset, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"errors": str(e)}, status=500)

    @swagger_auto_schema(
        request_body=CreateEventSerializer,
        responses={201: CreateEventSerializer},
    )
    def create(self, request):
        """
        Create a new Booking/Event.

        ## Request Body:
        - `hotel_id`: <int> The ID of the hotel (optional).
        - `timestamp`: <str|datetime> Timestamp of event in the format `%Y-%m-%dT%H:%M:%S` (optional).
        - `rpg_status`: <str|int> `1` for bookings | `2` for cancellations (optional).
        - `room_id`: <int> The ID for the room (optional).
        - `night_of_stay`: <str|date> The date of the night of stay in the format `%Y-%m-%d` (optional).

        ## Responses:
        - 201: Successful response.
        - 500: Error response.
        """
        serializer = CreateEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=500)
