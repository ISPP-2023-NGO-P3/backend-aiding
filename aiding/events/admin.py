from django.contrib import admin

from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "address",
                    "start_date", "end_date", "places")
    list_filter = ("title", "start_date", "end_date", "address")
    search_fields = ("title", "start_date", "end_date", "address")

admin.site.register(Event, EventAdmin)