from django.conf.urls import url

from .views import add_favorite, remove_favorite, FavoritesList


app_name = 'favorites'

urlpatterns = [
    url(r'^add/(?P<pk>\d+)-(?P<slug>[\w-]+)/$', add_favorite, name='add'),
    url(r'^remove/(?P<pk>\d+)-(?P<slug>[\w-]+)/$', remove_favorite, name='remove'),
    url(r'^list/$', FavoritesList.as_view(), name='list')
]
