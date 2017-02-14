from django import template

from ..models import Post


register = template.Library()


@register.inclusion_tag('blog/last.html')
def posts_last(number=3):
    posts = Post.objects.published()[:number]
    return {
        'posts': posts,
    }
