from django.contrib.sitemaps import Sitemap

from .models import UserProfile


class ProfileDetailSitemap(Sitemap):
    priority = 0.4
    changefreq = 'weekly'

    def items(self):
        return UserProfile.objects.filter(user__is_active=True)
