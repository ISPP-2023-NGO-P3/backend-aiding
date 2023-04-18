from django.urls import path

from .views import (ItemView, TypeView)

urlpatterns = [
    path('items/', ItemView.as_view()),
    path('items/<int:item_id>', ItemView.as_view()),

    path('types/', TypeView.as_view()),
    path('types/<int:type_id>', TypeView.as_view())
]
