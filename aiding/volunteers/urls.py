from django.urls import path
from .views import VolunteerManagement, TurnView

urlpatterns = [
    path('',VolunteerManagement.as_view()),
    path('<int:volunteer_id>',VolunteerManagement.as_view()),
    path('turns/',TurnView.as_view()),
    path('turns/<int:turn_id>/', TurnView.as_view()),
]