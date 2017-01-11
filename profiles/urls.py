from django.conf.urls import url

from . import recievers
from .views import DetailView, MaterialsView, ActivitiesView


app_name = 'profiles'

urlpatterns = [

    url(r'^(?P<slug>[\w.@+-]+)/detail/$', DetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w.@+-]+)/materials/$', MaterialsView.as_view(), name='materials'),
    url(r'^(?P<slug>[\w.@+-]+)/activities/$', ActivitiesView.as_view(), name='activities'),

]
