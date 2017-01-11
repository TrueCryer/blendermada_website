from django.conf.urls import url

from .views import MaterialDetailView, MaterialDownloadView, index, vote
from .feed import LatestMaterialsFeed


app_name = 'materials'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^detail/(?P<pk>\d+)-(?P<slug>[\w-]+)/$', MaterialDetailView.as_view(), name='detail'),
    url(r'^download/(?P<pk>\d+)-(?P<slug>[\w-]+).blend$', MaterialDownloadView.as_view(), name='download'),
    url(r'^vote/(?P<pk>\d+)-(?P<slug>[\w-]+)/(?P<score>[1-5])/$', vote, name='vote'),
    url(r'^feed.rss$', LatestMaterialsFeed(), name='feed'),
]
