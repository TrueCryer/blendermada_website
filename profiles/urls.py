from django.urls import path

from . import recievers
from .views import DetailView, MaterialsView, ActivitiesView


app_name = 'profiles'

urlpatterns = [

    path('<slug>/detail/', DetailView.as_view(), name='detail'),
    path('<slug>/materials/', MaterialsView.as_view(), name='materials'),
    path('<slug>/activities/', ActivitiesView.as_view(), name='activities'),

]
