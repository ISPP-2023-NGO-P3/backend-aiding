from django.urls import path
from .views import *

urlpatterns = [
    path('', PartnerManagement.as_view()),
    path('<int:id>', PartnerManagement.as_view()),
]