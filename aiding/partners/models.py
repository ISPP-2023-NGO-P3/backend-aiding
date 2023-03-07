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
    
    def total_all_donation(self):
        return sum(donation.total_donation for donation in self.donation.all())

    
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
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    periodicity = models.CharField(choices=[(p, p.value['name']) for p in DonationPeriodicity], max_length=20)
    total_donation = models.DecimalField(max_digits=12, decimal_places=2, null=True) 

    
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
                total_donation = self.amount * periods_passed

            self.total_donation = total_donation
            self.save(update_fields=['total_donation'])

    

        




