from django.conf.urls import url

from .views import (CategoryListView,
                    CategoryDetailView,
                    PostListView,
                    PostDetailView) 


app_name = 'blog'

urlpatterns = [
    url(
        r'^categories/$',
        CategoryListView.as_view(),
        name='category_list',
    ),
    url(
        r'^category/(?P<slug>[\w-]+)/$',
        CategoryDetailView.as_view(),
        name='category_detail',
    ),
    url(
        r'^$',
        PostListView.as_view(),
        name='post_list',
    ),
    url(
        r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[\w-]+)/$',
        PostDetailView.as_view(),
        name='post_detail',
    ),
]
