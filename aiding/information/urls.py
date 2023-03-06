from django.urls import path
from .views import ResourceView

urlpatterns = [
    path('resources/', ResourceView.as_view()),
    path('resources/<int:id>', ResourceView.as_view())

]