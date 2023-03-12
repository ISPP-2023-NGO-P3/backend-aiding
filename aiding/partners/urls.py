from django.urls import path
from .views import *
from .views import CommunicationView

urlpatterns = [
    path('', PartnerManagement.as_view()),
    path('<int:id>', PartnerManagement.as_view()),
    path('donation/', DonationView.as_view()),
    path('donation/<int:id>',DonationView.as_view()),
    path('<int:id>/receipt',download_receipt_xml),
    path('<int:partner_id>/communication/', CommunicationView.as_view()),
    path('<int:partner_id>/communication/<int:communication_id>',CommunicationView.as_view()),
]