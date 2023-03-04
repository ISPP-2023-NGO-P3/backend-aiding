from django.urls import path
from .views import *

urlpatterns = [
    path('partners/', PartnerManagement.as_view()),
    path('partners/<int:id>', PartnerManagement.as_view()),
]