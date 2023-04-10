from django.contrib import admin

from .models import Contact, User

admin.site.register(User)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'datetime', 'subject', 'message', 'isAnswered')
    list_filter =  ('email','phone', 'datetime', 'subject', 'isAnswered')
    search_fields = ('email', 'phone', 'datetime', 'subject')

admin.site.register(Contact, ContactAdmin)
