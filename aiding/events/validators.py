import datetime
from django.forms import ValidationError
import pytz

from aiding.settings import TIME_ZONE


def validate_event_start_date(start_date):
    try:
        now = datetime.datetime.utcnow()
        tz = pytz.timezone(TIME_ZONE)
        now_aware = pytz.utc.localize(now).astimezone(tz)
        if start_date < now_aware:
            raise ValidationError("Start date cannot be before current date and time.")
    except ValueError:
        raise ValidationError("Start date is not valid.")

def validate_event_end_date(start_date, end_date):
    try:
        if start_date > end_date:
            raise ValidationError("Start date cannot be after end date.")
    except ValueError:
        raise ValidationError("End date is not valid.")

def validate_event_is_started(start_date):
    try:
        now = datetime.datetime.utcnow()
        tz = pytz.timezone(TIME_ZONE)
        now_aware = pytz.utc.localize(now).astimezone(tz)
        if start_date > now_aware:
            raise ValidationError("Event has not started yet.")
    except ValueError:
        raise ValidationError("Start date is not valid.")