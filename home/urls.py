from django.urls import path
from .views import index, robots_txt, health_check, status, map_view

urlpatterns = [
    path('', index, name='home'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('health/', health_check, name='health_check'),
    path('status/', status, name='status'),
    path('map/', map_view, name='map'),
]