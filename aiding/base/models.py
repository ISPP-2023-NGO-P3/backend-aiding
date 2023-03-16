from django.db import models

# Create your models here.



class Section(models.Model):
    name = models.CharField(unique=True, blank=False, null=False, max_length=100)
    active = models.BooleanField(blank=False, null=False, default=False)
