from django import template

from ..models import Material, Category


register = template.Library()


@register.inclusion_tag('materials/search.html')
def materials_search():
    categories = Category.objects.all()
    return {
        'engines': Material.ENGINES,
        'categories': categories,
    }


@register.inclusion_tag('materials/stars.html')
def stars(material):
    rating = material.rating
    full_stars = int(round(rating))
    empty_stars = 5 - full_stars
    return {
        'stars': ['star'] * full_stars + ['star-empty'] * empty_stars
    }


@register.inclusion_tag('materials/last.html')
def materials_last(number=2):
    materials = Material.objects.published()[:number]
    return {
        'title': 'Latest materials',
        'materials': materials,
    }


@register.inclusion_tag('materials/last.html')
def materials_random(number=2):
    materials = Material.objects.published().order_by('?')[:number]
    return {
        'title': 'Random materials',
        'materials': materials,
    }
