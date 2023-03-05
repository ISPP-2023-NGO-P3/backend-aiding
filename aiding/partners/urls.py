from django.urls import path
from .views import *

urlpatterns = [
    path('donation/', DonationView.as_view()),
    path('donation/<int:id>',DonationView.as_view()),
    path('partners/', PartnerManagement.as_view()),
    path('partners/<int:id>', PartnerManagement.as_view()),

]