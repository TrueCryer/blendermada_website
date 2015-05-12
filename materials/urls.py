from django.conf.urls import patterns, url

from . import recievers
from .views import MaterialDetailView, MaterialDownloadView, index, vote
from .feed import LatestMaterialsFeed


urlpatterns = patterns('',
    url(r'^$', index, name='materials_index'),
    url(r'^detail/(?P<pk>\d+)-(?P<slug>[\w-]+)/$', MaterialDetailView.as_view(), name='materials_detail'),
    url(r'^download/(?P<pk>\d+)-(?P<slug>[\w-]+).blend$', MaterialDownloadView.as_view(), name='materials_download'),
    url(r'^vote/(?P<pk>\d+)-(?P<slug>[\w-]+)/(?P<score>[1-5])/$', vote, name='materials_vote'),
    url(r'^feed.rss$', LatestMaterialsFeed(), name='materials_feed'),
)
