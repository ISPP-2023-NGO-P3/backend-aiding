from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Volunteer(models.Model):
    SITUATION_CHOICES = (
        ('Ok','Ok'),
        ('necesitaFormacion','Necesita formación'),
        ('necesitaComplemento','Necesita complemento'),
    )

    ROL_CHOICES = (
        ('Voluntario','Voluntario'),
        ('Supervisor','Supervisor'),
        ('Capitan','Capitán'),
    )

    STATE_CHOICES = (
        ('Activo','Activo'),
        ('Activo','Inactivo'),
    )

    name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    num_volunteer=models.IntegerField(blank=False,unique=True)
    nif=models.CharField(max_length=9, unique=True, blank=False)
    place=models.CharField(max_length=150, blank=False)
    phone=models.CharField(max_length=15, unique=True, blank=False)
    email = models.EmailField(unique=True, blank=False)
    state = models.CharField(max_length=8, choices=STATE_CHOICES, default='Activo')
    situation = models.CharField(max_length=25,choices=SITUATION_CHOICES)
    rol = models.CharField(max_length=15,choices=ROL_CHOICES)
    observations= models.CharField(max_length=250,blank=True)
    computerKnowledge=models.BooleanField(blank=False, default=False)
    truckKnowledge=models.BooleanField(blank=False, default=False)
    warehouseKnowledge=models.BooleanField(blank=False, default=False)
    otherKnowledge= models.CharField(max_length=250,blank=True)

class Turn(models.Model):
    date = models.DateField(null=False)
    startTime = models.TimeField(null=False)
    endTime = models.TimeField(null=False)
    volunteers = models.ManyToManyField(Volunteer)
    
    def clean(self):
        super().clean()
        if self.startTime >= self.endTime:
            raise ValidationError('La hora de inicio debe ser anterior a la hora de fin')
        if self.date < timezone.localdate():
            raise ValidationError('La fecha debe ser posterior o igual a la fecha actual')

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)