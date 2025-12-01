from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from django.contrib.sitemaps.views import sitemap

from home import views
from home.sitemaps import StaticViewSitemap


sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('sitemap.xml', sitemap, {"sitemaps": sitemaps}, name='sitemap'),
]


handler404 = 'home.views.custom_404'
handler500 = 'home.views.custom_500'