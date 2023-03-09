from django.urls import path
from .views import SectionView, AdvertisementView, MultimediaView, AdvertisementSectionView

urlpatterns = [
    path('sections/', SectionView.as_view()),
    path('sections/<int:id>',SectionView.as_view()),

    path('advertisements/', AdvertisementView.as_view()),
    path('advertisements/<int:id>',AdvertisementView.as_view()),

    path('multimedias/', MultimediaView.as_view()),
    path('multimedias/<int:id>',MultimediaView.as_view()),

    # CUSTOM ENDPOINTS

     path('sections/<int:section_id>/advertisements/',AdvertisementSectionView.as_view()),
]