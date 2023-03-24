from django.contrib import admin

from .models import Contact, User, Notification

admin.site.register(User)
admin.site.register(Notification)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'datetime', 'subject', 'message', 'isAnswered')
    list_filter =  ('email','phone', 'datetime', 'subject', 'isAnswered')
    search_fields = ('email', 'phone', 'datetime', 'subject')

admin.site.register(Contact, ContactAdmin)
