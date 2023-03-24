from django.urls import path
from .views import VolunteerManagement

urlpatterns = [
    path('',VolunteerManagement.as_view()),
    path('<int:volunteer_id>',VolunteerManagement.as_view()),
]