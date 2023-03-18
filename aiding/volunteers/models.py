from django.db import models

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
    num_volunteer=models.IntegerField(blank=False)
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
    