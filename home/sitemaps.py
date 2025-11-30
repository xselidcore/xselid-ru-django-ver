from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['home'] 

    def location(self, item):
        return reverse(item)

class DynamicViewSitemap(Sitemap):
    priority = 0.6
    changefreq = 'daily'

    def items(self):
        return Page.objects.all()  

    def lastmod(self, obj):
        return obj.updated_at
