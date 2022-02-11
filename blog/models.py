from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import PublicManager


class Category(models.Model):
    """Category model."""
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        db_table = 'blog_categories'
        ordering = ('title',)

    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        return reverse('blog:category_detail', kwargs={'slug': self.slug})


class Post(models.Model):
    """Post model."""
    STATUS_CHOICES = (
        ('d', _('Draft')),
        ('p', _('Public')),
    )
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique_for_date='publish')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='posts',
        blank=True, null=True, on_delete=models.DO_NOTHING,
    )
    body = models.TextField(_('body'))
    tease = models.TextField(
        _('tease'),
        blank=True,
        help_text=_('Concise text suggested. Does not appear in RSS feed.'),
    )
    status = models.CharField(
        _('status'),
        max_length=2,
        choices=STATUS_CHOICES,
        default='d',
    )
    allow_comments = models.BooleanField(_('allow comments'), default=True)
    publish = models.DateTimeField(_('publish'), default=timezone.now)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name='posts',
    )

    objects = PublicManager()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ('-publish',)
        get_latest_by = 'publish'

    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={
            'year': self.publish.year,
            'month': self.publish.month,
            'day': self.publish.day,
            'slug': self.slug,
        })

    def get_previous_post(self):
        return self.get_previous_by_publish(status='p')

    def get_next_post(self):
        return self.get_next_by_publish(status='p')
