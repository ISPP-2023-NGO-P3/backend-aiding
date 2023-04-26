from django.db import models
from django.forms import ValidationError
from .validators import validate_nif
from base.models import User

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
        ('nuevo','Nuevo'),
        ('posibleSupervisor','Posible supervisor'),
        ('posibleCapitan','Posible capitán'),
        ('posibleVoluntarioEstructura','Posible voluntario de estructura'),
    )

    STATE_CHOICES = (
        ('Activo','Activo'),
        ('Inactivo','Inactivo'),
    )

    name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    nif=models.CharField(max_length=9, unique=True, blank=False,validators=[validate_nif])
    place=models.CharField(max_length=150, blank=False)
    phone=models.CharField(max_length=15, unique=True, blank=False)
    email = models.EmailField(unique=True, blank=False)
    state = models.CharField(max_length=8, choices=STATE_CHOICES, default='Activo')
    situation = models.CharField(max_length=35,choices=SITUATION_CHOICES)
    rol = models.CharField(max_length=30,choices=ROL_CHOICES)
    postal_code = models.CharField(max_length=5, blank=False)
    observations= models.CharField(max_length=250,blank=True)
    computerKnowledge=models.BooleanField(blank=False, default=False)
    truckKnowledge=models.BooleanField(blank=False, default=False)
    warehouseKnowledge=models.BooleanField(blank=False, default=False)
    otherKnowledge= models.CharField(max_length=250,blank=True)

class Turn(models.Model):
    title = models.CharField(max_length=100, blank=False, unique=True)
    date = models.DateField(null=False)
    startTime = models.TimeField(null=False)
    endTime = models.TimeField(null=False)
    draft = models.BooleanField(default=False)
    supervisor = models.ForeignKey(User, on_delete= models.CASCADE, related_name='supervisor')

class VolunteerTurn(models.Model):
    volunteer= models.ForeignKey(Volunteer, on_delete= models.CASCADE, related_name='volunteer')
    turn= models.ForeignKey(Turn, on_delete= models.CASCADE, related_name='turn')

    def clean(self):
        volunteerTurns=VolunteerTurn.objects.filter(volunteer=self.volunteer,turn=self.turn)
        if len(volunteerTurns) > 0:
            raise ValidationError('Este voluntario ya tiene asignado el mismo turno')
    