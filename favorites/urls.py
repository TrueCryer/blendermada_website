from django.urls import path

from .views import add_favorite, remove_favorite, FavoritesList


app_name = 'favorites'

urlpatterns = [
    path('add/<int:pk>-<slug:slug>/', add_favorite, name='add'),
    path('remove/<int:pk>-<slug:slug>/', remove_favorite, name='remove'),
    path('list/', FavoritesList.as_view(), name='list')
]
