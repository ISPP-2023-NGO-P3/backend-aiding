from django.urls import path
from .views import *

urlpatterns = [
    path('', PartnerManagement.as_view()),
    path('<int:id>', PartnerManagement.as_view()),
    path('<int:id>/donation', DonationView.as_view()),
    path('donation/<int:id>',DonationView.as_view()),
    path('<int:id>/donation',get_don_part),
    path('<int:id>/receipt',download_receipt_xml),
]