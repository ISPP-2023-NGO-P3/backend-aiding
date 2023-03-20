from django.contrib import admin

from .models import Volunteer

class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('name','last_name','num_volunteer','nif','place','rol')
    list_filter = ('place','rol')
    search_fields = ('name','last_name','num_volunteer','nif')

admin.site.register(Volunteer,VolunteerAdmin)
