from datetime import date
from enum import Enum
from django.db import models
from .validators import validate_date, validate_dni, validate_iban
from django.db.models import Sum
from enum import Enum

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
    phone2 = models.CharField(max_length=15, blank=True)
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
    observations = models.CharField(max_length=500, blank=True)

    
class DonationPeriodicity(Enum):
    MONTHLY = {'name': 'MENSUAL', 'days': 30}
    QUARTERLY = {'name': 'TRIMESTRAL', 'days': 90}
    SEMIANNUAL  = {'name': 'SEMESTRAL', 'days': 180}
    ANNUAL = {'name': 'ANUAL', 'days': 365}

    def get_periodicity_days(self):
        return self.value['days']

class Donation(models.Model):
    partner = models.OneToOneField(Partners, on_delete = models.CASCADE, related_name='donation')
    date = models.DateField()
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    periodicity = models.CharField(choices=[(p.value['name'], p.name) for p in DonationPeriodicity], max_length=20)

    
    def total_donation(self):

        f_date = date.replace(day=31, month=12,  year=self.date.year)
        numero_dias = (f_date-self.date).days()

        numero_periodos = int(numero_dias/DonationPeriodicity[self.periodicity].get_periodicity_days())

        return numero_periodos*self.amount

class Communication(models.Model):
    COMMUNICATION_TYPE = (
        ('TELEFÓNICA','TELEPHONIC'),
        ('TELEMÁTICA','TELEMATIC'),
        ('PERSONAL' , 'PERSONAL'),
        ('EMAIL' ,'EMAIL'),
    )

    partner = models.ForeignKey(Partners, on_delete= models.CASCADE, related_name='communication')
    date = models.DateField(null = False)
    communication_type = models.CharField(max_length=25, choices= COMMUNICATION_TYPE, blank= False)
    description = models.TextField(blank= False, null=False,max_length=255)