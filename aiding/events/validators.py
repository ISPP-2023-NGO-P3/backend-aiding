import datetime
from django.forms import ValidationError
import pytz

from aiding.settings import TIME_ZONE


def validate_event_date(start_date_str, end_date_str):
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S")
    now = datetime.datetime.utcnow()
    tz = pytz.timezone(TIME_ZONE)
    now_aware = pytz.utc.localize(now).astimezone(tz)
    start_date_aware = tz.localize(start_date)
    end_date_aware = tz.localize(end_date)
    if start_date_aware < now_aware:
        raise ValidationError("Start date cannot be before current date and time.")
    if end_date_aware < now_aware:
        raise ValidationError("End date cannot be before current date and time.")
    if start_date_aware > end_date_aware:
        raise ValidationError("Start cannot be after end date.")
