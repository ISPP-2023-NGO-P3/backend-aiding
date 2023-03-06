from django.contrib import admin
from .models import *
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id','title','description','number', 'street', 'city', 'latitude', 'longitude')
    list_filter = ('id','title','description','number', 'street', 'city', 'latitude', 'longitude')
    search_fields = ('id','title','description','number', 'street', 'city', 'latitude', 'longitude')

admin.site.register(Resource, ResourceAdmin)