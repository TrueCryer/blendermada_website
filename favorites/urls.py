from django.conf.urls import url

from .views import add_favorite, remove_favorite, FavoritesList


urlpatterns = [
    url(r'^add/(?P<pk>\d+)-(?P<slug>[\w-]+)/$', add_favorite, name='favorites_add'),
    url(r'^remove/(?P<pk>\d+)-(?P<slug>[\w-]+)/$', remove_favorite, name='favorites_remove'),
    url(r'^list/$', FavoritesList.as_view(), name='favorites_list')
]
