from django.urls import path
from .views import *

urlpatterns = [
    path('sections/', SectionView.as_view()),
    path('sections/<int:id>',SectionView.as_view()),

    path('advertisements/', AdvertisementView.as_view()),
    path('advertisements/<int:id>',AdvertisementView.as_view()),

    path('multimedias/', MultimediaView.as_view()),
    path('multimedias/<int:id>',MultimediaView.as_view(), name="v2"),

]