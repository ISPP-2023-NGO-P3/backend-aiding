from django.contrib import admin
from .models import *

class PartnersAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'dni', 'phone', 'email', 'province', 'iban', 'state')
    list_filter = ('name', 'last_name', 'dni', 'phone', 'email', 'province', 'iban', 'state')
    search_fields = ('name', 'last_name', 'dni', 'phone', 'email', 'province', 'iban', 'state')

admin.site.register(Partners, PartnersAdmin)