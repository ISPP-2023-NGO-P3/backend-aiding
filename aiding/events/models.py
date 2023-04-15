from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ValidationError

from .validators import validate_event_start_date, validate_event_end_date
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST as ST_400
from rest_framework.status import HTTP_408_REQUEST_TIMEOUT as ST_408


class Event(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    start_date = models.DateTimeField(blank=False, validators=[validate_event_start_date])
    end_date = models.DateTimeField(blank=False)
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
        if not self.start_date:
            raise ValidationError("Start date is required.")
        if not self.end_date:
            raise ValidationError("End date is required.")
        validate_event_end_date(self.start_date, self.end_date)

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

#APUNTARSE A UN EVENTO
    def available_places(self):
        total_places = self.places
        bookings = self.bookings.count()
        available_places = total_places - bookings

        return f'{available_places} places available of {total_places} places.' 

    def is_full(self):
        return self.available_places() == 0

class Booking(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'phone', 'event')