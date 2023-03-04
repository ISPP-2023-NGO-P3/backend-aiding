from django.urls import path
from .views import *

urlpatterns = [
    path('donations/<int:donation_id>/receipt',download_receipt_xml),
]