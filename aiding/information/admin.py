from django.contrib import admin
from .models import Advertisement, Resource, Section, Multimedia


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id','title','description','number', 'street', 'city', 'latitude', 'longitude')
    list_filter = ('id','title','description','number', 'street', 'city', 'latitude', 'longitude')
    search_fields = ('id','title','description','number', 'street', 'city', 'latitude', 'longitude')

    def save_model(self, request, obj, form, change):
        
        if change:
            old_obj = self.model.objects.get(pk=obj.pk)
            if old_obj.number != obj.number or old_obj.street != obj.street or old_obj.city != obj.city or old_obj.latitude != obj.latitude or old_obj.longitude != obj.longitude:
                obj.latitude, obj.longitude = Resource.get_coordinates(self, obj.street, obj.number, obj.city)
        super().save_model(request, obj, form, change)
            
admin.site.register(Resource, ResourceAdmin)
