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
from django.views.generic import RedirectView
from .views import *
from . import views

urlpatterns = [
    path('/', RedirectView.as_view(url='/kiosk/overview')),
    path('lakis/', LakiListView.as_view(), name='laki-list'),
    path('kiosk/', views.KioskList, name='kiosk-list'),
    path('kiosk/overview', views.KioskOverview, name='kiosk-overview'),
    path('kiosk/zelt/<int:pk>', views.KioskDetail, name='kiosk-detail'),
    path('lakis/<int:pk>/', LakiDetailView.as_view(), name='laki-detail'),
    path('kiosk/<int:pk>', views.LakiKiosk, name='laki-kiosk'),
    path('zelt/<int:pk>', views.ZeltDetail, name='zelt-detail'),
]
