from __future__ import unicode_literals

from django.contrib.sitemaps import Sitemap
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse_lazy

from .models import Material
from .settings import MATERIALS_PER_PAGE


class MaterialListSitemap(Sitemap):
    priority = 0.6
    changefreq = 'daily'
    
    def items(self):
        objects = Material.objects.published()
        paginator = Paginator(objects, MATERIALS_PER_PAGE)
        return paginator.page_range

    def location(self, page):
        return '%s?page=%s' % (reverse_lazy('materials_index'), page)


class MaterialDetailSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'
    
    def items(self):
        return Material.objects.published()
