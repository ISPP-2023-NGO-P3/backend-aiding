from django.urls import path
from .views import ContactView

urlpatterns = [
    path('contact/', ContactView.as_view()),
    path('contact/<int:contact_id>/', ContactView.as_view()),

]