from django.db import models
from .validators import validate_file_extension

# Create your models here.

class Section(models.Model):
    name = models.CharField(unique=True, blank=False, null=False, max_length=100)

class Advertisement(models.Model):
    title = models.CharField(unique=True, blank=False, null=False, max_length=200)
    description = models.TextField(blank= False, null=False, max_length=500)
    url = models.URLField(null= True, blank= True)
    section = models.ForeignKey(Section, related_name='section', on_delete = models.CASCADE)
    front_page = models.ImageField(null=False, upload_to='information/media', validators=[validate_file_extension])

class Multimedia(models.Model):
    advertisement = models.ForeignKey(Advertisement, related_name='advertisement', on_delete = models.CASCADE)
    multimedia = models.ImageField(blank=True, null=True, upload_to='information/media')
    description = models.TextField(blank= True, null=True,max_length=255)