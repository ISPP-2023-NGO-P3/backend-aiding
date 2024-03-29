from django.urls import path

from .views import (EventView, FutureEventView, StartedEventView, EventBookingView)

urlpatterns = [
    path('', EventView.as_view()),
    path('<int:event_id>', EventView.as_view()),

    path('programed/', FutureEventView.as_view()),
    path('started/', StartedEventView.as_view()),

    path('<int:event_id>/booking/', EventBookingView.as_view()),
]
