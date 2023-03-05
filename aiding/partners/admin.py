from django.contrib import admin
from .models import *

class PartnersAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'dni', 'phone', 'email', 'province', 'iban', 'state')
    list_filter = ('name', 'last_name', 'dni', 'phone', 'email', 'province', 'iban', 'state')
    search_fields = ('name', 'last_name', 'dni', 'phone', 'email', 'province', 'iban', 'state')

admin.site.register(Partners, PartnersAdmin)

class DonationAdmin(admin.ModelAdmin):
    list_display = ('partner', 'date', 'donation_type', 'amount','periodicity','total_donation')
    list_filter = ('partner', )
    search_fields = ('partner', )

admin.site.register(Donation, DonationAdmin)

