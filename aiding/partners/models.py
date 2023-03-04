from datetime import date, timedelta
from django.db import models
from django.db.models import Sum


from enum import Enum

class Partner(models.Model):
    name = models.CharField(max_length=100)


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
    partner = models.ForeignKey(Partner, on_delete = models.CASCADE, related_name='donation')
    date = models.DateField()
    donation_type = models.CharField(choices=[(t, t.value) for t in DonationType], max_length=20)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    periodicity = models.CharField(choices=[(p, p.value['name']) for p in DonationPeriodicity], max_length=20)
    total_donation = models.DecimalField(max_digits=12, decimal_places=2) #total de donacion al año, de que fecha a que fecha, cuando necesitan exportar el total de donacion

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super(Donation, self).save(*args, **kwargs)
        if is_new or 'amount' in kwargs['update_fields']:
            #Calculating total donation for non-periodic 
            if self.periodicity == DonationPeriodicity.NONE.name:
                #Calculate total donation based on previous donations
                previous_donations = Donation.objects.filter(
                    partner=self.partner, periodicity=DonationPeriodicity.NONE.name,
                    date__lt=self.date
                ).aggregate(Sum('amount'))['amount__sum'] or 0
                total_donation = previous_donations + (self.amount or 0)
            else:
                first_day_of_donation_month = self.date.replace(day=1)
                first_day_of_month = date.today()
                periods_passed = (
                    (first_day_of_month - first_day_of_donation_month).days // self.get_periodicity_days()
                )
                total_donation = self.amount * periods_passed
                
            self.total_donation = total_donation
            self.save(update_fields=['total_donation'])

