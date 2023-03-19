from django.urls import path
from .views import ContactView

urlpatterns = [
    path('contacts/', ContactView.as_view()),
    path('contacts/<int:contact_id>/', ContactView.as_view()),

]