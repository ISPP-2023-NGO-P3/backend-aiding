from django.urls import path
from .views import *

urlpatterns = [
    path('communication/', CommunicationView.as_view()),
    path('communication/<int:id>',CommunicationView.as_view()),
    path('partner/', PartnerView.as_view()),
    path('partner/<int:id>',PartnerView.as_view()),
]