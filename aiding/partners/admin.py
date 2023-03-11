from django.contrib import admin
from .models import *

class PartnersAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'dni', 'phone1', 'phone2', 'birthdate', 'sex', 'email', 'address', 'postal_code', 'township', 'province', 'language', 'iban', 'account_holder', 'state')
    list_filter = ('name', 'last_name', 'dni', 'phone1', 'phone2', 'birthdate', 'sex', 'email', 'address', 'postal_code', 'township', 'province', 'language', 'iban', 'account_holder', 'state')
    search_fields = ('name', 'last_name', 'dni', 'phone1', 'phone2', 'birthdate', 'sex', 'email', 'address', 'postal_code', 'township', 'province', 'language', 'iban', 'account_holder', 'state')

admin.site.register(Partners, PartnersAdmin)

class DonationAdmin(admin.ModelAdmin):
    list_display = ('partner', 'date', 'donation_type', 'amount','periodicity','total_donation')
    list_filter = ('partner', )
    search_fields = ('partner', )

admin.site.register(Donation, DonationAdmin)

