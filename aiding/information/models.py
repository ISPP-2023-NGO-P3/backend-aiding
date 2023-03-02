from django.db import models

# Create your models here.

class Section(models.Model):
    name = models.CharField(blank=False, null=False, max_length=100)
class Advertisement(models.Model):
    title = models.CharField(unique=True, blank=False, null=False, max_length=100)
    description = models.TextField(blank= False, null=False,max_length=255)
    url = models.URLField(null= False, blank= False)
    section = models.ForeignKey(Section, related_name='section', on_delete = models.CASCADE)
class Multimedia(models.Model):
    advertisement = models.ForeignKey(Advertisement, related_name='multimedia', on_delete = models.CASCADE)
    multimedia = models.FileField(upload_to='information/media')
    description = models.TextField(blank= True, null=True,max_length=255)