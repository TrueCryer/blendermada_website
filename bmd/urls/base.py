from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.views.generic import TemplateView

from bmd.sitemaps import sitemaps


urlpatterns = patterns('',

    url(r'^admin/', include('smuggler.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^materials/', include('materials.urls')),
    url(r'^account/', include('accounts.urls')),
    url(r'^profiles/', include('profiles.urls')),
    url(r'^uploads/', include('uploads.urls')),
    url(r'^captcha/', include('captcha.urls')),

    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^addon/$', TemplateView.as_view(template_name='addon.html'), name='addon'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),

    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),

    url(r'^api/materials/', include('materials.api')),
    url(r'^api/uploads/', include('uploads.api')),

)
