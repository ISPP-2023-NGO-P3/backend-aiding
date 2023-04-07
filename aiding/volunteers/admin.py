from django.contrib import admin

from .models import Volunteer, Turn, VolunteerTurn

class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('name','last_name','num_volunteer','nif','place','rol')
    list_filter = ('place','rol')
    search_fields = ('name','last_name','num_volunteer','nif')

admin.site.register(Volunteer,VolunteerAdmin)
admin.site.register(Turn)
admin.site.register(VolunteerTurn)