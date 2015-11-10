from django import template

from ..models import Favorite


register = template.Library()

@register.simple_tag
def favorited(material, user):
    return Favorite.objects.filter(material=material, user=user).count() > 0
