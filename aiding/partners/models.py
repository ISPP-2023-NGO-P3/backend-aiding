from django.db import models
from .validators import *

class Partners(models.Model):
    STATE_CHOICES = (
        ('Activo', 'active'),
        ('Inactivo', 'inactive'),
    )

    SEX_CHOICES = (
        ('Hombre', 'men'),
        ('Mujer', 'women'),
        ('Ninguno', 'none'),
    )

    LANGUAGE_CHOICES = (
        ('Español', 'spanish'),
        ('Catalán', 'catalan'),
    )

    name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    dni = models.CharField(max_length=9, unique=True, blank=False, validators=[validate_dni])
    phone1 = models.CharField(max_length=15, unique=True, blank=False)
    phone2 = models.CharField(max_length=15)
    birthdate = models.DateField(blank=False, validators=[validate_date])
    sex = models.CharField(max_length=25, choices=SEX_CHOICES)
    email = models.EmailField(unique=True, blank=False)
    address = models.CharField(max_length=150, blank=False)
    postal_code = models.CharField(max_length=5, blank=False)
    township = models.CharField(max_length=50, blank=False)
    province = models.CharField(max_length=50, blank=False)
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES, blank=False)
    iban = models.CharField(max_length=34, unique=True, blank=False, validators=[validate_iban])
    account_holder = models.CharField(max_length=100, blank=False)
    state = models.CharField(max_length=8, choices=STATE_CHOICES, default='active')