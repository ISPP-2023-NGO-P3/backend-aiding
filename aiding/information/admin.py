from django.contrib import admin



from .models import *
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id','title','description','number', 'street', 'city', 'latitude', 'longitude')
    list_filter = ('id','title','description','number', 'street', 'city', 'latitude', 'longitude')
    search_fields = ('id','title','description','number', 'street', 'city', 'latitude', 'longitude')

    def save_model(self, request, obj, form, change):
        
        if not obj.latitude  or not obj.longitude:
            obj.latitude, obj.longitude = Resource.get_coordinates(self, obj.street, obj.number, obj.city)
        super().save_model(request, obj, form, change)
            
admin.site.register(Resource, ResourceAdmin)