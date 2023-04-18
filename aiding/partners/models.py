from datetime import date
from enum import Enum
from django.db import models
from django.forms import ValidationError
from .validators import validate_date, validate_dni, validate_iban

dict_dates= {'MENSUAL':30,'TRIMESTRAL':90,'SEMESTRAL':180,'ANUAL':365}

class Partners(models.Model):
    STATE_CHOICES = (
        ('Activo','Activo'),
        ('Inactivo','Inactivo'),
    )

    SEX_CHOICES = (
        ('men','Hombre'),
        ('women','Mujer'),
        ('none','Ninguno'),
    )

    LANGUAGE_CHOICES = (
        ('spanish','Español'),
        ('catalan','Catalán'),
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
    state = models.CharField(max_length=8, choices=STATE_CHOICES, default='Activo')

class DonationPeriodicity(Enum):
    MONTHLY = {'name': 'MENSUAL', 'days': 30}
    QUARTERLY = {'name': 'TRIMESTRAL', 'days': 90}
    SEMIANNUAL  = {'name': 'SEMESTRAL', 'days': 180}
    ANNUAL = {'name': 'ANUAL', 'days': 365}

    def get_periodicity_days(self):
        return self.value['days']

class Donation(models.Model):
    partner = models.ForeignKey(Partners, on_delete= models.CASCADE, related_name='donation')
    start_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    periodicity = models.CharField(choices=[(p.value['name'], p.name) for p in DonationPeriodicity], max_length=20)
    year = models.IntegerField(default=date.today().year, editable=False)


    def clean(self):
        existing_donation = Donation.objects.filter(partner=self.partner, year=self.year).first()
        if existing_donation and existing_donation.id != self.id:
            raise ValidationError('Ya existe una donación para este socio y año.')
    
    class Meta:
        unique_together = ('partner', 'year')

    def total_donation(self):
        amount=self.amount
        end_date = date(self.start_date.year, 12, 10)
        if self.periodicity == DonationPeriodicity.ANNUAL.value['name']:
            return amount
        start_date = self.start_date
        if start_date.day > 14:
            start_date = date(start_date.year, start_date.month + 1, 10)
        else:
            start_date = date(start_date.year, start_date.month, 10)
        num_days = (end_date - start_date).days
        periodicity= dict_dates[self.periodicity]
        num_periods = num_days // periodicity
        return amount * num_periods
    
        
class Communication(models.Model):
    COMMUNICATION_TYPE = (
            ('TELEFÓNICA', 'TELEPHONIC'),
            ('TELEMÁTICA', 'TELEMATIC'),
            ('PERSONAL', 'PERSONAL'),
            ('EMAIL' ,'EMAIL'),
        )

    partner = models.ForeignKey(Partners, on_delete= models.CASCADE, related_name='communication')
    date = models.DateField(null = False)
    communication_type = models.CharField(max_length=25, choices= COMMUNICATION_TYPE, blank= False)
    description = models.TextField(blank= False, null=False,max_length=255)

class CSVFile(models.Model):
    file = models.FileField(upload_to="import_partners")


    
