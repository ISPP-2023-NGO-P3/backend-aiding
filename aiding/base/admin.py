from django.contrib import admin

from .models import Contact, User, Notification

admin.site.register(User)
admin.site.register(Notification)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'datetime', 'subject', 'message', 'isAnswered')
    list_filter =  ('email', 'datetime', 'subject', 'isAnswered')
    search_fields = ('email', 'datetime', 'subject')

admin.site.register(Contact, ContactAdmin)
