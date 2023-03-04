from django.contrib import admin
from .models import *

class DonationAdmin(admin.ModelAdmin):
    list_display = ('partner', 'date', 'donation_type', 'amount','periodicity','total_donation')
    list_filter = ('partner', )
    search_fields = ('partner', )

admin.site.register(Donation, DonationAdmin)
