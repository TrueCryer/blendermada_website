from django.urls import path

from .views import (CategoryListView,
                    CategoryDetailView,
                    PostListView,
                    PostDetailView)


app_name = 'blog'

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/',
         CategoryDetailView.as_view(), name='category_detail'),
    path('', PostListView.as_view(), name='post_list'),
    path(
        '<int:year>/<int:month>/<int:day>/<slug:slug>/',
        PostDetailView.as_view(),
        name='post_detail',
    ),
]
