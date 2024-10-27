import csv
import time
import pytz
import subprocess

from datetime import datetime

from django.db import transaction

from provider.models import Event


BASE_DIR = "/app/main"
CSV_FILE = f"{BASE_DIR}/provider/data/data.csv"

events_data: list[dict] = list()

utc = pytz.timezone("utc")


def generate_event_instance(
    hotel_id: int,
    room_id: int,
    event_timestamp: datetime,
    night_of_stay: datetime,
    rpg_status: str,
    room_reservation_id: str,
):
    _event_timestamp = utc.localize(
        datetime.strptime(event_timestamp, "%Y-%m-%d %H:%M:%S")
    )
    _night_of_stay = utc.localize(datetime.strptime(night_of_stay, "%Y-%m-%d"))

    return Event(
        hotel_id=hotel_id,
        room_id=room_id,
        event_timestamp=_event_timestamp,
        night_of_stay=_night_of_stay,
        rpg_status=rpg_status,
        room_reservation_id=room_reservation_id,
    )


def read_csv_file(_file):
    try:
        with open(_file, "r") as f:
            csv_reader = csv.reader(f)
            _headers = next(csv_reader)
            _csv_headers = [i for i in _headers]  # Get headers
            for row in csv_reader:
                entry = dict()
                for i, h in enumerate(_csv_headers):
                    entry[str(h)] = row[i]
                events_data.append(entry)
    except Exception as e:
        print(f"ERROR: {e}")


def bulk_create_events(_events: list[dict]):
    def generate_bulk():
        bulk_ls = []
        for _event in _events:
            instance = generate_event_instance(
                room_id=_event["id"],
                hotel_id=_event["hotel_id"],
                event_timestamp=_event["event_timestamp"],
                night_of_stay=_event["night_of_stay"],
                rpg_status=_event["status"],
                room_reservation_id=_event["room_reservation_id"],
            )
            bulk_ls.append(instance)
        return bulk_ls

    start_time = time.perf_counter()

    with transaction.atomic():
        try:
            print("Bulk creating events ...")
            events_to_create = generate_bulk()
            Event.objects.bulk_create(events_to_create)
            print(f"Done in {time.perf_counter() - start_time} second(s).")
        except Exception as e:
            print(f"ERROR: {e}")


def delete_events():
    start_time = time.perf_counter()
    print("Deleted events ...")
    Event.objects.all().delete()
    print(f"Done in {time.perf_counter() - start_time} second(s).")


def initialize_db():
    subprocess.call(["python", f"{BASE_DIR}/manage.py", "migrate"])


def run(*args):
    initialize_db()
    delete_events()
    read_csv_file(CSV_FILE)
    bulk_create_events(events_data)
