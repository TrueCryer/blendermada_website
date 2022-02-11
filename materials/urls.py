from django.urls import path

from .views import MaterialDetailView, MaterialDownloadView, index, vote
from .feed import LatestMaterialsFeed


app_name = 'materials'

urlpatterns = [

    path('', index, name='index'),

    path('detail/<int:pk>-<slug:slug>/',
         MaterialDetailView.as_view(),
         name='detail'),

    path('download/<int:pk>-<slug:slug>.blend',
         MaterialDownloadView.as_view(),
         name='download'),

    path('vote/<int:pk>-<slug:slug>/<score>/',
         vote,
         name='vote'),

    path('feed.rss', LatestMaterialsFeed(), name='feed'),
]
