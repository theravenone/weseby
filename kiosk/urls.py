"""weseby URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.urls import path, include
from .views import *
from . import views

urlpatterns = [
    path('lakis/', LakiListView.as_view(), name='laki-list'),
    path('kiosk/', views.KioskList, name='kiosk-list'),
    path('<int:pk>/', LakiDetailView.as_view(), name='laki-detail'),
    path('<int:pk>/kiosk', views.LakiKiosk, name='laki-kiosk'),
]
