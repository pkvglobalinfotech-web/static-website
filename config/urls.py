"""
URL configuration for PKV Global Infotech website.
Admin panel removed — all site data is in static_data.py.
"""
from django.urls import path, include

urlpatterns = [
    path('', include('website.urls')),
]
