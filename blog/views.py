from __future__ import unicode_literals

from django.views.generic import DetailView, ListView, DateDetailView

from .models import Category, Post 


class CategoryListView(ListView):
    model = Category


class CategoryDetailView(DetailView):
    model = Category


class PostListView(ListView):
    queryset = Post.objects.published()


class PostDetailView(DateDetailView):
    queryset = Post.objects.published()
    date_field = 'publish'
    month_format = '%m'
