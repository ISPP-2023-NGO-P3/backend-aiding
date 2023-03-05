from django.db import models
from .validators import *

class Partners(models.Model):
    STATE_CHOICES = (
        ('ACTIVE', 'active'),
        ('INACTIVE', 'inactive'),
    )

    name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    dni = models.CharField(max_length=9, unique=True, blank=False, validators=[validate_dni])
    phone = models.CharField(max_length=15, unique=True, blank=False)
    email = models.EmailField(unique=True, blank=False)
    province = models.CharField(max_length=50, blank=False)
    iban = models.CharField(max_length=34, unique=True, blank=False, validators=[validate_iban])
    state = models.CharField(max_length=8, choices=STATE_CHOICES, default='active')