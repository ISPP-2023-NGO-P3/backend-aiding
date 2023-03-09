from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.http import JsonResponse
from geopy.geocoders import Nominatim


# Create your models here.

class Resource(models.Model):
    title = models.CharField(blank=False, null=False, max_length=100)
    description = models.CharField(blank=False, max_length=255)
    
    street = models.CharField(blank=False, max_length=255)
    number = models.CharField(null=True, blank=True, max_length=10)
    city = models.CharField(blank=False, max_length=100)
    additional_comments = models.CharField(blank=True, max_length=255)

    latitude = models.FloatField(blank=True, max_length=255, validators=[MaxValueValidator(90), MinValueValidator(-90)])
    longitude = models.FloatField(blank=True, max_length=255, validators=[MaxValueValidator(180), MinValueValidator(-180)])

    def get_coordinates(self, street, number, city):
        address = street
                   
        if number:
            if number.isdigit():
                if int(number)>0:
                    address += ", " + number
                else:
                    return JsonResponse({'error': "Number must be positive or null"})
            else:
                return JsonResponse({'error': "Number must be positive or null"})

        address += ", "+ city
        geolocator = Nominatim(user_agent="aiding")
        location = geolocator.geocode(address)

        if location:
            latitude = location.latitude
            longitude = location.longitude
        else:
            return JsonResponse({'error': "Address not found"})
        print(latitude)
        print(longitude)

        return latitude, longitude