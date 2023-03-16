from django.urls import path
from .views import DonationView, PartnerManagement, CommunicationView, download_receipt_xml, get_don_part

urlpatterns = [
    path('', PartnerManagement.as_view()),
    path('<int:id>', PartnerManagement.as_view()),
    path('<int:id>/donation', DonationView.as_view()),
    path('<int:partner_id>/communication/', CommunicationView.as_view()),
    path('<int:partner_id>/communication/<int:communication_id>',CommunicationView.as_view()),
    path('donation/', DonationView.as_view()),
    path('<int:id>/donation',get_don_part),
    path('<int:id>/receipt',download_receipt_xml),
]