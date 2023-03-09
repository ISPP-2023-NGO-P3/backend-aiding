from django.contrib import admin
from .models import Advertisement, Section, Multimedia

# Register your models here.

class SectionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name', )
    search_fields = ('name', )

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'url', 'section')
    list_filter = ('title', )
    search_fields = ('title', )

class MultimediaAdmin(admin.ModelAdmin):
    list_display = ('advertisement', 'multimedia', 'description')
    list_filter = ('advertisement', )
    search_fields = ('advertisement', )

admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Multimedia, MultimediaAdmin)