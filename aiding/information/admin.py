from django.contrib import admin
from rest_framework.response import Response

from .models import Advertisement, Multimedia, Resource, Section


class SectionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name', )
    search_fields = ('name', )


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'section')
    list_filter = ('title', )
    search_fields = ('title', )


class MultimediaAdmin(admin.ModelAdmin):
    list_display = ('advertisement', 'multimedia', 'description')
    list_filter = ('advertisement', )
    search_fields = ('advertisement', )


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'number',
                    'street', 'city', 'latitude', 'longitude')
    list_filter = ('id', 'title', 'description', 'number',
                   'street', 'city', 'latitude', 'longitude')
    search_fields = ('id', 'title', 'description', 'number',
                     'street', 'city', 'latitude', 'longitude')

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = self.model.objects.get(pk=obj.pk)
            if old_obj.number != obj.number or old_obj.street != obj.street or old_obj.city != obj.city or old_obj.latitude != obj.latitude or old_obj.longitude != obj.longitude:
                coord = Resource.get_coordinates(
                    self, obj.street, obj.number, obj.city)
                if isinstance(coord, Response):
                    return coord
                else:
                    obj.latitude, obj.longitude = coord[0], coord[1]
        super().save_model(request, obj, form, change)


admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Multimedia, MultimediaAdmin)
admin.site.register(Resource, ResourceAdmin)
