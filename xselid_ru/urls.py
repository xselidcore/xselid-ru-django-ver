from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import handler404
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
]


handler404 = 'home.views.custom_404'
handler500 = 'home.views.custom_500'