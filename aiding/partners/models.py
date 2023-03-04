from django.db import models

class Partners(models.Model):
    STATE_CHOICES = (
        ('ALTA', 'alta'),
        ('BAJA', 'baja'),
    )

    name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    dni = models.CharField(max_length=9, unique=True, blank=False)
    phone = models.CharField(max_length=15, unique=True, blank=False)
    email = models.EmailField(unique=True, blank=False)
    province = models.CharField(max_length=50, blank=False)
    iban = models.CharField(max_length=34, unique=True, blank=False)
    state = models.CharField(max_length=4, choices=STATE_CHOICES, default='alta')
