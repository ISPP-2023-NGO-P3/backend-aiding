import datetime
import json
from django.forms import ValidationError
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
import pytz

from rest_framework import views
from rest_framework.response import Response

from aiding.settings import TIME_ZONE
from .validators import validate_event_start_date, validate_event_end_date
from rest_framework.status import HTTP_200_OK as ST_200
from rest_framework.status import HTTP_201_CREATED as ST_201
from rest_framework.status import HTTP_204_NO_CONTENT as ST_204
from rest_framework.status import HTTP_404_NOT_FOUND as ST_404
from rest_framework.status import HTTP_400_BAD_REQUEST as ST_400
from rest_framework.status import HTTP_409_CONFLICT as ST_409


from .models import Event


class CsrfExemptMixin:
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class EventView(CsrfExemptMixin, views.APIView):
    def get(self, request, event_id=0):
        if event_id > 0:
            events = list(Event.objects.filter(id=event_id).values())
            if len(events) > 0:
                event = events[0]
                return Response(data=event, status=ST_200)
            else:
                data = {"message": "Event not found..."}
                return Response(data=data, status=ST_404)
        else:
            events = list(Event.objects.values())
            if len(events) > 0:
                return Response(data=events, status=ST_200)
            else:
                data = {"message": "No events found..."}
                return Response(data=data, status=ST_404)

    def post(self, request):
        jd = json.loads(request.body)
        try:
            user_tz = pytz.timezone(jd["userTimezone"])
            start_date = user_tz.localize(datetime.datetime.strptime(jd["start_date"], "%Y-%m-%d %H:%M:%S"))
            end_date = user_tz.localize(datetime.datetime.strptime(jd["end_date"], "%Y-%m-%d %H:%M:%S"))
            validate_event_start_date(start_date)
            validate_event_end_date(start_date, end_date)
        except ValidationError as e:
            return Response(data=e.message, status=ST_400)
        try:
            street = jd["street"]
            number = jd["number"]
            city = jd["city"]

            coord = Event.get_coordinates(self, street, number, city)
            if isinstance(coord, Response):
                return coord

            server_tz = pytz.timezone(TIME_ZONE)
            start_date_server = start_date.astimezone(server_tz)
            end_date_server = end_date.astimezone(server_tz)

            Event.objects.create(
                title=jd["title"],
                description=jd["description"],
                start_date=start_date_server,
                end_date=end_date_server,
                places=jd["places"],
                street=street,
                number=number,
                city=city,
                latitude=coord[0],
                longitude=coord[1],
            )
            data = {"message": "Success"}
            return Response(data=data, status=ST_201)
        except IntegrityError:
            error = {
                "error": "Event already exists",
            }
            return Response(data=error, status=ST_409)

    def put(self, request, event_id):
        jd = json.loads(request.body)
        events = list(Event.objects.filter(id=event_id).values())
        if len(events) > 0:
            event = Event.objects.get(id=event_id)
            if not is_future_event(event):
                data = {"message": "Event is not active..."}
                return Response(data=data, status=ST_400)
            try:
                user_tz = pytz.timezone(jd["userTimezone"])
                start_date = user_tz.localize(datetime.datetime.strptime(jd["start_date"], "%Y-%m-%d %H:%M:%S"))
                end_date = user_tz.localize(datetime.datetime.strptime(jd["end_date"], "%Y-%m-%d %H:%M:%S"))

                validate_event_start_date(start_date)
                validate_event_end_date(start_date, end_date)
            except ValidationError as e:
                return Response(data=e.message, status=ST_400)
            try:
                event.title = jd["title"]
                event.description = jd["description"]
                event.start_date = start_date
                event.end_date = end_date
                event.places = jd["places"]

                street = jd["street"]
                number = jd["number"]
                city = jd["city"]

                coord = Event.get_coordinates(self, street, number, city)
                if isinstance(coord, Response):
                    return coord

                event.street = street
                event.number = number
                event.city = city

                event.latitude = coord[0]
                event.longitude = coord[1]

                event.save()
                data = {"message": "Success"}
                return Response(data=data, status=ST_200)
            except IntegrityError as e:
                return Response(data=e.message, status=ST_400)

    def delete(self, request, event_id):
        events = list(Event.objects.filter(id=event_id).values())
        if len(events) > 0:
            event = Event.objects.get(id=event_id)
            event.delete()
            data = {"message": "Success"}
            return Response(data=data, status=ST_204)
        else:
            data = {"message": "Event not found..."}
            return Response(data=data, status=ST_404)

class FutureEventView(CsrfExemptMixin, views.APIView):
    def get(self, request):
        events = list(Event.objects.filter(
            start_date__gte=timezone.now()).values())
        if len(events) > 0:
            return Response(data=events, status=ST_200)
        else:
            data = {"message": "No events found..."}
            return Response(data=data, status=ST_404)


class StartedEventView(CsrfExemptMixin, views.APIView):
    def get(self, request):
        now = datetime.datetime.utcnow()
        tz = pytz.timezone(TIME_ZONE)
        now_aware = pytz.utc.localize(now).astimezone(tz)

        events = list(
            Event.objects.filter(
                start_date__lte=now_aware, end_date__gte=now_aware
            ).values()
        )

        if len(events) > 0:
            return Response(data=events, status=ST_200)
        else:
            data = {"message": "No events found..."}
            return Response(data=data, status=ST_404)

def is_future_event(event):
    if event:
        start_date = event.start_date
        now = datetime.datetime.utcnow()
        tz = pytz.timezone(TIME_ZONE)
        now_aware = pytz.utc.localize(now).astimezone(tz)
        return start_date > now_aware
    else:
        raise ValidationError("Event not found")
