from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from materials.models import Material
from .models import Favorite


@login_required
def add_favorite(request, pk, slug):
    mat = get_object_or_404(Material, pk=pk, slug=slug)
    fav, created = Favorite.objects.get_or_create(
        user=request.user, material=mat,
    )
    fav.save()
    return HttpResponseRedirect(reverse('materials_detail', kwargs={'pk':pk, 'slug':slug}))


@login_required
def remove_favorite(request, pk, slug):
    return HttpResponseRedirect(reverse('favorites_list'))


class FavoritesList(ListView):
    def get_queryset(self):
        user = self.request.user
        return user.favorites.all().select_related('material').prefetch_related('material__category')