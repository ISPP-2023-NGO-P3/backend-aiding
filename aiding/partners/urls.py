from django.urls import path
from .views import *

urlpatterns = [
    path('donation/', DonationView.as_view()),
    path('donation/<int:id>',DonationView.as_view()),
    path('', PartnerManagement.as_view()),
    path('<int:id>', PartnerManagement.as_view()),
    path('communication/', CommunicationView.as_view()),
    path('communication/<int:id>',CommunicationView.as_view()),
]