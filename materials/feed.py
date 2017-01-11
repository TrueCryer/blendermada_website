from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.contrib.syndication.views import Feed
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import iri_to_uri

from .models import Material


description = """
<img src="{0}" />
<p>Category: {1}</p>
<p>Engine: {2}</p>
<p>Description: {3}</p>
"""


def add_domain(domain, url, secure=False):
    protocol = 'https' if secure else 'http'
    if url.startswith('//'):
        # Support network-path reference (see #16753) - RSS requires a protocol
        url = '{protocol}:{url}'.format(protocol=protocol, url=url)
    elif not (url.startswith('http://')
            or url.startswith('https://')
            or url.startswith('mailto:')):
        url = iri_to_uri('{protocol}://{domain}{url}'.format(protocol=protocol, domain=domain, url=url))
    return url


class LatestMaterialsFeed(Feed):
    title = 'New materials'
    link = reverse_lazy('materials:index')
    description = 'New materials on Blendermada'

    def items(self):
        return Material.objects.order_by('-date')[:8]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        current_site = get_current_site(self.request)
        return description.format(
            add_domain(current_site.domain, item.thumb_medium.url, self.request.is_secure()),
            item.category,
            item.get_engine_display(),
            item.description,
        )

    def get_feed(self, obj, request):
        self.request = request
        return super(LatestMaterialsFeed, self).get_feed(obj, request)
