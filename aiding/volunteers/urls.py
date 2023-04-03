from django.urls import path
from .views import VolunteerManagement, TurnView, VolunteerTurnView

urlpatterns = [
    path('',VolunteerManagement.as_view()),
    path('<int:volunteer_id>',VolunteerManagement.as_view()),
    path('turns/',TurnView.as_view()),
    path('turns/<int:turn_id>/', TurnView.as_view()),
    path('volunteerTurns/',VolunteerTurnView.as_view()),
    path('volunteerTurns/<int:volunteerTurn_id>/', VolunteerTurnView.as_view()),

]