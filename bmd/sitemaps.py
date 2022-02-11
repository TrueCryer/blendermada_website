from django.contrib import sitemaps
from django.urls import reverse_lazy

from materials.sitemaps import MaterialListSitemap, MaterialDetailSitemap
from profiles.sitemaps import ProfileDetailSitemap


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.4
    changefreq = 'daily'

    def items(self):
        return ['home', 'addon', 'about']

    def location(self, item):
        return reverse_lazy(item)


sitemaps = {
    'static': StaticViewSitemap,
    'material-list': MaterialListSitemap,
    'material-detail': MaterialDetailSitemap,
    'profile-detail': ProfileDetailSitemap,
}
