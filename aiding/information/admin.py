from django.contrib import admin
from .models import *
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title','description','number', 'street', 'city', 'latitude', 'longitude')
    list_filter = ('title','description','number', 'street', 'city', 'latitude', 'longitude')
    search_fields = ('title','description','number', 'street', 'city', 'latitude', 'longitude')

admin.site.register(Resource, ResourceAdmin)