from django.urls import path
from .views import *

urlpatterns = [
    path('<int:partner_id>/receipt',download_receipt_xml),
    path('donation/', DonationView.as_view()),
    path('donation/<int:id>',DonationView.as_view()),
    path('', PartnerManagement.as_view()),
    path('<int:id>', PartnerManagement.as_view()),
]