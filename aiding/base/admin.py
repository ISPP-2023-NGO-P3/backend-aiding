from django.contrib import admin
from .models import User, Notification

admin.site.register(User)
admin.site.register(Notification)
from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'datetime', 'subject', 'message', 'isAnswered')
    list_filter =  ('email', 'datetime', 'subject', 'isAnswered')
    search_fields = ('email', 'datetime', 'subject')

admin.site.register(Contact, ContactAdmin)
