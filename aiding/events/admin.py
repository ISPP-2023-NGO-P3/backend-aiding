from django.contrib import admin
from rest_framework.response import Response
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "description",
                    "start_date", "end_date", "places")
    list_filter = ("title", "start_date", "end_date")
    search_fields = ("title", "start_date", "end_date")

    def save_model(self, request, obj, form, change):
        jd = request.POST

        street = jd["street"]
        number = jd["number"]
        city = jd["city"]

        coord = Event.get_coordinates(self, street, number, city)
        if isinstance(coord, Response):
            return coord
        else:
            obj.latitude, obj.longitude = coord[0], coord[1]
        super().save_model(request, obj, form, change)


admin.site.register(Event, EventAdmin)