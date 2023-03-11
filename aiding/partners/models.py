from datetime import date
from decimal import Decimal
from django.db import models
from validators import validate_date, validate_dni, validate_iban
from django.db.models import Sum
from enum import Enum

class Partners(models.Model):
    STATE_CHOICES = (
        ('Active', 'active'),
        ('Inactive', 'inactive'),
    )

    SEX_CHOICES = (
        ('Men', 'men'),
        ('Women', 'women'),
        ('None', 'none'),
    )

    LANGUAGE_CHOICES = (
        ('Spanish', 'spanish'),
        ('Catalan', 'catalan'),
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
    
class DonationType(Enum):
    FOOD = 'FOOD'
    MONETARY = 'MONETARY'
    
class DonationPeriodicity(Enum):
    MONTHLY = {'name': 'MONTHLY', 'days': 30}
    QUARTERLY = {'name': 'QUARTERLY', 'days': 90}
    SEMIANNUAL  = {'name': 'SEMIANNUAL', 'days': 180}
    ANNUAL = {'name': 'ANNUAL', 'days': 365}
    NONE = {'name': 'NONE', 'days': 0}

    def get_periodicity_days(self):
        return self.value['days']

class Donation(models.Model):
    partner = models.ForeignKey(Partners, on_delete = models.CASCADE, related_name='donation')
    date = models.DateField()
    donation_type = models.CharField(choices=[(t, t.value) for t in DonationType], max_length=20)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    periodicity = models.CharField(choices=[(p, p.value['name']) for p in DonationPeriodicity], max_length=20)
    total_donation = models.DecimalField(max_digits=12, decimal_places=2, null=True) #total de donacion al año, de que fecha a que fecha, cuando necesitan exportar el total de donacion
    

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super(Donation, self).save(*args, **kwargs)
        if is_new or ('update_fields' in kwargs and 'amount' in kwargs['update_fields']):
            if self.periodicity == DonationPeriodicity.NONE.name:
                previous_donations = Donation.objects.filter(
                    partner=self.partner,
                    periodicity=DonationPeriodicity.NONE.name,
                    date__lt=self.date
                ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
                total_donation = previous_donations + Decimal(str(self.amount or 0))
            else:
                first_day_of_donation_month = self.date.replace(day=1, month=self.date.month, year=self.date.year)
                first_day_of_month = date.today()
                periods_passed = (
                    (first_day_of_month - first_day_of_donation_month).days // DonationPeriodicity[self.periodicity].get_periodicity_days()
                )
                if self.donation_type == DonationType.MONETARY.name:
                    total_donation = self.amount * periods_passed
                else:
                    total_donation = self.amount

            self.total_donation = total_donation
            self.save(update_fields=['total_donation'])    

