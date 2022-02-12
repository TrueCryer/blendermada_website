from bmd.sitemaps import sitemaps
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.urls import include, path

from django.contrib import admin
admin.autodiscover()


urlpatterns = [

    path('admin/', admin.site.urls),
    path('materials/', include('materials.urls')),
    path('account/', include('accounts.urls')),
    path('profiles/', include('profiles.urls')),
    path('uploads/', include('uploads.urls')),
    path('captcha/', include('captcha.urls')),
    path('favorites/', include('favorites.urls')),
    path('blog/', include('blog.urls')),

    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('addon/', TemplateView.as_view(template_name='addon.html'), name='addon'),
    path('addon/changelog/',
         TemplateView.as_view(template_name='changelog.html'), name='addon_changelog'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),

    path('sitemap.xml', sitemap_view, {
        'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain'), name='robots'),

    path('api/materials/', include('materials.api')),
    path('api/uploads/', include('uploads.api')),

]
