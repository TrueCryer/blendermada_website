from django.conf.urls import url

from . import recievers
from .views import DetailView, MaterialsView, ActivitiesView


urlpatterns = [

    url(r'^(?P<slug>[\w.@+-]+)/detail/$', DetailView.as_view(), name='profiles_detail'),
    url(r'^(?P<slug>[\w.@+-]+)/materials/$', MaterialsView.as_view(), name='profiles_materials'),
    url(r'^(?P<slug>[\w.@+-]+)/activities/$', ActivitiesView.as_view(), name='profiles_activities'),

]
