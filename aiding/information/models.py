from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST as ST_400
from rest_framework.status import HTTP_404_NOT_FOUND as ST_404
from rest_framework.status import HTTP_408_REQUEST_TIMEOUT as ST_408

from .validators import validate_file_extension


class Section(models.Model):
    name = models.CharField(unique=True, blank=False, null=False, max_length=100)
    active = models.BooleanField(blank=False, null=False, default=False)


class Advertisement(models.Model):
    title = models.CharField(unique=True, blank=False, null=False, max_length=200)
    description = models.TextField(blank=False, null=False, max_length=5000)
    url = models.URLField(null=True, blank=True)
    section = models.ForeignKey(
        Section, related_name="section", on_delete=models.CASCADE
    )
    front_page = models.ImageField(
        null=False,
        upload_to="information/advertisements",
        default="information/media/default.png",
        validators=[validate_file_extension],
    )


class Multimedia(models.Model):
    advertisement = models.ForeignKey(
        Advertisement, related_name="advertisement", on_delete=models.CASCADE
    )
    multimedia = models.ImageField(
        blank=True, null=True, upload_to="information/multimedia"
    )
    description = models.TextField(blank=True, null=True, max_length=255)

class Resource(models.Model):
    RESOURCE_TYPE = (
        ('Asociación de vecinos','neighborhood_association'),
        ('Asociación de mayores','seniors_association'),
        ('Residencia','nursing_home'),
    )
    title = models.CharField(blank=False, null=False, max_length=100)
    description = models.CharField(blank=False, max_length=255)
    contact_phone = models.CharField(null=True, blank=True, max_length=15)
    street = models.CharField(blank=False, max_length=255)
    number = models.CharField(null=True, blank=True, max_length=10)
    city = models.CharField(blank=False, max_length=100)
    resource_type = models.CharField(max_length=25, choices=RESOURCE_TYPE)

    additional_comments = models.CharField(blank=True, max_length=255)

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

    def save(self, *args, **kwargs):
        self.position = f'[{self.latitude}, {self.longitude}]'
        super(Resource, self).save(*args, **kwargs)

    def get_coordinates(self, street, number, city):
        address = street
        if number:
            if number.isdigit():
                if int(number) > 0:
                    address += ", " + number
                else:
                    error = "Number must be positive or null"
                    return Response(data=error, status=ST_400)
            else:
                error = "Number must be positive or null"
                return Response(data=error, status=ST_400)

        address += ", " + city
        geolocator = Nominatim(user_agent="aiding")
        location = geolocator.geocode(address)
        try:
            location = geolocator.geocode(address, timeout=10)
        except GeocoderTimedOut as error_timeout:
            error = "GeocodeTimedOut: " + str(error_timeout)
            return Response(data=error, status=ST_408)

        if location:
            latitude = location.latitude
            longitude = location.longitude
        else:
            error = "Address not found."
            return Response(data=error, status=ST_404)
        return latitude, longitude
