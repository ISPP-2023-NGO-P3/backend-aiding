from django.contrib import admin
from .models import Partners, Donation, Communication, CSVFile

class PartnersAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'dni', 'phone1', 'phone2', 'birthdate', 'sex', 'email', 'address', 'postal_code', 'township', 'province', 'language', 'iban', 'account_holder', 'state')
    list_filter = ('name', 'last_name', 'dni', 'phone1', 'phone2', 'birthdate', 'sex', 'email', 'address', 'postal_code', 'township', 'province', 'language', 'iban', 'account_holder', 'state')
    search_fields = ('name', 'last_name', 'dni', 'phone1', 'phone2', 'birthdate', 'sex', 'email', 'address', 'postal_code', 'township', 'province', 'language', 'iban', 'account_holder', 'state')

admin.site.register(Partners, PartnersAdmin)

class DonationAdmin(admin.ModelAdmin):
    list_display = ('partner', 'date', 'amount','periodicity')
    list_filter = ('partner', )
    search_fields = ('partner', )

admin.site.register(Donation, DonationAdmin)

class CommunicationAdmin(admin.ModelAdmin):
    list_display=('partner', 'date', 'communication_type', 'description')
    list_filter = ('partner', 'date', 'description', 'communication_type')
    search_fields =('partner', 'date', 'description', 'communication_type')

admin.site.register(Communication, CommunicationAdmin)