from django.urls import path
from .views import DonationView, PartnerManagement, CommunicationView

urlpatterns = [
    path('donation/', DonationView.as_view()),
    path('donation/<int:id>',DonationView.as_view()),
    path('', PartnerManagement.as_view()),
    path('<int:id>', PartnerManagement.as_view()),
    path('<int:partner_id>/communication/', CommunicationView.as_view()),
    path('<int:partner_id>/communication/<int:id>',CommunicationView.as_view()),
]