from datetime import date, timedelta, timezone
from decimal import Decimal
from django.db import models
from django.db.models import Sum
from enum import Enum

class Partners(models.Model):
    STATE_CHOICES = (
        ('ACTIVO', 'activo'),
        ('INACTIVO', 'inactivo'),
    )

    name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    dni = models.CharField(max_length=9, unique=True, blank=False)
    phone = models.CharField(max_length=15, unique=True, blank=False)
    email = models.EmailField(unique=True, blank=False)
    province = models.CharField(max_length=50, blank=False)
    iban = models.CharField(max_length=34, unique=True, blank=False)
    state = models.CharField(max_length=8, choices=STATE_CHOICES, default='active')
    
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
    periodicity = models.CharField(choices=[(p.name, p.value['name']) for p in DonationPeriodicity], max_length=20)

    
    def total_donation(self):

        f_date = date.replace(day=31, month=12,  year=self.date.year)
        numero_dias = (f_date-self.date).days()

        numero_periodos = int(numero_dias/DonationPeriodicity[self.periodicity].get_periodicity_days())

        return numero_periodos*self.amount