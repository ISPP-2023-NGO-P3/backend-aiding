"""aiding URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from .views import LogoutView, NotificationView, UserView, ContactView, RoleView, RolesView, RegisterView
from django.urls import path

urlpatterns = [
    path('logout/', LogoutView.as_view()),
    path('register/', RegisterView.as_view()),
    path('users/', UserView.as_view()),
    path('users/<int:user_id>', UserView.as_view()),
    path('contacts/', ContactView.as_view()),
    path('contacts/<int:contact_id>/', ContactView.as_view()),
    path('notifications/', NotificationView.as_view()),
    path('user/role/', RoleView.as_view()),
    path('user/roles/', RolesView.as_view()),
]