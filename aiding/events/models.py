from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import validate_event_date
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST as ST_400
from rest_framework.status import HTTP_404_NOT_FOUND as ST_404
from rest_framework.status import HTTP_408_REQUEST_TIMEOUT as ST_408


class Event(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    places = models.PositiveIntegerField()

    street = models.CharField(blank=False, max_length=255)
    number = models.CharField(null=True, blank=True, max_length=10)
    city = models.CharField(blank=False, max_length=100)

    latitude = models.FloatField(
        null=True,
        blank=True,
        max_length=255,
        validators=[MaxValueValidator(90), MinValueValidator(-90)],
    )
    longitude = models.FloatField(
        null=True,
        blank=True,
        max_length=255,
        validators=[MaxValueValidator(180), MinValueValidator(-180)],
    )

    position = models.CharField(max_length=50, blank=True)

    def clean(self):
        validate_event_date(self.start_date, self.end_date)

    def save(self, *args, **kwargs):
        self.position = f'[{self.latitude}, {self.longitude}]'
        super(Event, self).save(*args, **kwargs)

    def get_coordinates(self, street, number, city):
        address = street
        if number:
            if number.isdigit():
                if int(number) > 0:
                    address += ", " + number
                else:
                    error = {"error": "Number must be positive or null."}
                    return Response(data=error, status=ST_400)
            else:
                error = {"error": "Number must be positive or null."}
                return Response(data=error, status=ST_400)

        address += ", " + city
        geolocator = Nominatim(user_agent="aiding")
        try:
            location = geolocator.geocode(address, timeout=20)
        except GeocoderTimedOut as error_timeout:
            error = {"error": "GeocodeTimedOut: " + str(error_timeout)}
            return Response(data=error, status=ST_408)

        if location:
            latitude = location.latitude
            longitude = location.longitude
        else:
            error = {"error": "Address not found."}
            return Response(data=error, status=ST_400)

        return latitude, longitude
