from django.urls import path
from .views import *

urlpatterns = [
    path('donation/', DonationView.as_view()),
    path('donation/<int:id>',DonationView.as_view()),
    path('partner/', PartnerView.as_view()),
    path('partner/<int:id>',PartnerView.as_view()),
]