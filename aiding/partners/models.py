from django.db import models

from enum import Enum

# Create your models here.
class ComunicationType(Enum):
    TELEFONICA = 'TELEFÓNICA'
    TELEMATICA = 'TELEMÁTICA'
    PERSONAL = 'PERSONAL'
    EMAIL = 'EMAIL'

class Comunication(models.Model):
    date = models.DateField(null = False)
    comunication_type = models.CharField(
        choices=[(t, t.value) for t in ComunicationType],
        max_length=20,
        null=False)
