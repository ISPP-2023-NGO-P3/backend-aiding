import datetime
from django.forms import ValidationError
from dateutil.parser import parse
import pytz

from aiding.settings import TIME_ZONE


def validate_event_date(start_date, end_date):
    start_date = str(start_date)
    end_date = str(end_date)
    now = datetime.datetime.now()
    tz = pytz.timezone(TIME_ZONE)
    now_aware = str(tz.localize(now))
    if start_date < now_aware:
        raise ValidationError(
            "Start date cannot be before current date and time."
        )
    if end_date < now_aware:
        raise ValidationError(
            "End date cannot be before current date and time."
        )
    if start_date > end_date:
        raise ValidationError(
            "Start cannot be after end date."
        )
