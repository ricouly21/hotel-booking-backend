from datetime import datetime

from django.db import models


RPG_STATUS_CHOICES = (("1", "booking"), ("2", "cancellation"))


class Event(models.Model):
    event_id = models.BigAutoField(primary_key=True)
    hotel_id = models.IntegerField(null=True, blank=True)
    room_id = models.IntegerField(null=True, blank=True)
    event_timestamp = models.DateTimeField(null=True, blank=True)
    night_of_stay = models.DateTimeField(null=True, blank=True)
    rpg_status = models.CharField(
        max_length=1, choices=RPG_STATUS_CHOICES, null=True, blank=True
    )
    room_reservation_id = models.CharField(max_length=36, null=True, blank=True)

    class Meta:
        ordering = ["pk"]

    def __str__(self) -> str:
        return f"{self.event_id} | {self.hotel_id} | {self.room_id} | {self.room_reservation_id}"

    @property
    def id(self):
        return f"{self.event_id}"

    @property
    def timestamp(self):
        return f"{self.event_timestamp.isoformat()}"
