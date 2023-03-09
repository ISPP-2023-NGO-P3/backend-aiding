from django.db import models

from enum import Enum

# Create your models here.
class Partner(models.Model):
    name = models.CharField(max_length=100)

class CommunicationType(Enum):
    TELEFONICA = 'TELEFÓNICA'
    TELEMATICA = 'TELEMÁTICA'
    PERSONAL = 'PERSONAL'
    EMAIL = 'EMAIL'

class Communication(models.Model):
    partner = models.ForeignKey(Partner, on_delete= models.CASCADE, related_name='communication')
    date = models.DateField(null = False)
    communication_type = models.CharField(
        choices=[(t, t.value) for t in CommunicationType],
        max_length=20,
        null=False)
    description = models.TextField(blank= False, null=False,max_length=255)
    
    
