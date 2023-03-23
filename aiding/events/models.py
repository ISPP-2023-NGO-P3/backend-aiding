from django.db import models

from .validators import validate_event_date


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    address = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    places = models.IntegerField()

    def clean(self):
        validate_event_date(self.start_date, self.end_date)

    ### Aclarar que address se sustituirá o no por una asociacion a Recursos
    ### Hará falta una asociación a los usuarios que quieran asistir y así se
    ### podrá controlar el número de plazas disponibles