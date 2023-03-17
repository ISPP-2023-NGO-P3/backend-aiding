from django.urls import path

from .views import (AdvertisementSectionView, AdvertisementView,
                    MultimediaView, ResourceView, SectionView, ResourceTypeView, ResourceResourceTypeView)

urlpatterns = [
    path('sections/', SectionView.as_view()),
    path('sections/<int:section_id>', SectionView.as_view()),

    path('advertisements/', AdvertisementView.as_view()),
    path('advertisements/<int:advertisement_id>', AdvertisementView.as_view()),

    path('multimedias/', MultimediaView.as_view()),
    path('multimedias/<int:multimedia_id>', MultimediaView.as_view()),

    path('resources/', ResourceView.as_view()),
    path('resources/<int:resource_type_id>', ResourceView.as_view()),

    path('resource_types/', ResourceTypeView.as_view()),
    path('resource_types/<int:resource_type_id>', ResourceTypeView.as_view()),

    # CUSTOM ENDPOINTS

    path('sections/<int:section_id>/advertisements/',
         AdvertisementSectionView.as_view()),

    path('resource_types/<int:resource_type_id>/resources/',
         ResourceResourceTypeView.as_view())

]
