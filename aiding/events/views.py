import json
from django.forms import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

from rest_framework import views
from rest_framework.response import Response
from datetime import date
from .validators import validate_event_date
from rest_framework.status import HTTP_200_OK as ST_200
from rest_framework.status import HTTP_201_CREATED as ST_201
from rest_framework.status import HTTP_204_NO_CONTENT as ST_204
from rest_framework.status import HTTP_404_NOT_FOUND as ST_404
from rest_framework.status import HTTP_400_BAD_REQUEST as ST_400

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
            validate_event_date(jd["start_date"], jd["end_date"])
        except ValidationError as e:
            return Response(data=e.message, status=ST_400)
        Event.objects.create(
            title=jd["title"],
            description=jd["description"],
            address=jd["address"],
            start_date=jd["start_date"],
            end_date=jd["end_date"],
            places=jd["places"],
        )
        data = {"message": "Success"}
        return Response(data=data, status=ST_201)

    def put(self, request, event_id):
        jd = json.loads(request.body)
        events = list(Event.objects.filter(id=event_id).values())
        if len(events) > 0:
            event = Event.objects.get(id=event_id)
            try:
                validate_event_date(jd["start_date"], jd["end_date"])
            except ValidationError as e:
                return Response(data=e.message, status=ST_400)
            try:
                event.title = jd["title"]
                event.description = jd["description"]
                event.address = jd["address"]
                event.start_date = jd["start_date"]
                event.end_date = jd["end_date"]
                event.places = jd["places"]
                event.save()
                data = {"message": "Success"}
                return Response(data=data, status=ST_200)
            except IntegrityError as e:
                return Response(data=e.message, status=ST_400)


class FutureEventView(CsrfExemptMixin, views.APIView):
    def get(self, request):
        events = list(Event.objects.filter(start_date__gte=date.today()).values())
        if len(events) > 0:
            return Response(data=events, status=ST_200)
        else:
            data = {"message": "No events found..."}
            return Response(data=data, status=ST_404)


class StartedEventView(CsrfExemptMixin, views.APIView):
    def get(self, request):
        events = list(
            Event.objects.filter(
                start_date__lte=date.today(), end_date__gte=date.today()
            ).values()
        )
        if len(events) > 0:
            return Response(data=events, status=ST_200)
        else:
            data = {"message": "No events found..."}
            return Response(data=data, status=ST_404)
