from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Resource(models.Model):
    title = models.CharField(blank=False, null=False, max_length=100)
    description = models.CharField(blank=False, max_length=255) 
    
    street = models.CharField(blank=False, max_length=100)
    number = models.PositiveIntegerField(blank=True)
    city = models.CharField(blank=False, max_length=100)
    additional_comments = models.CharField(blank=True, max_length=255)

    latitude = models.FloatField(blank=False, validators=[MaxValueValidator(90), MinValueValidator(-90)])
    longitude = models.FloatField(blank=False, validators=[MaxValueValidator(180), MinValueValidator(-180)])

    
