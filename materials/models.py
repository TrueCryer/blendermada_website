import html2text
from os import path
from uuid import uuid4
import tempfile

from PIL import Image

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from core.mail import send_templated_mail


def get_image_filename(instance, filename):
    ext = path.splitext(filename)[1]
    return path.join('materials', 'images', '{name}{ext}'.format(name=uuid4(), ext=ext))


def get_storage_filename(instance, filename):
    ext = path.splitext(filename)[1]
    return path.join('materials', 'storages', '{name}{ext}'.format(name=uuid4(), ext=ext))


class Category(models.Model):

    name = models.CharField(_('name'), max_length=25)
    slug = models.SlugField(_('slug'))

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)


class Author(models.Model):

    name = models.CharField(_('name'), max_length=50)
    email = models.EmailField(_('e-mail'), max_length=50)

    class Meta:
        verbose_name = _('author')
        verbose_name_plural = _('authors')

    def __str__(self):
        return '{name}, <{email}>'.format(name=self.name, email=self.email)


class MaterialManager(models.Manager):

    use_for_related_fields = True

    def published(self, **kwargs):
        return self.filter(draft=False, **kwargs)


class Material(models.Model):

    ENGINES = (
        ('int', 'Blender Internal'),
        ('cyc', 'Cycles'),
        ('lux', 'Lux Render'),
        ('yfr', 'YafaRay'),
        ('oct', 'Octane'),
        ('nox', 'NOX Render'),
    )

    engine = models.CharField('Render engine', max_length=3, choices=ENGINES)
    category = models.ForeignKey(
        Category, related_name='materials', on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=20)
    slug = models.SlugField('Slug')
    description = models.TextField('Description', blank=True)
    author = models.ForeignKey(
        Author,
        related_name='materials',
        blank=True, null=True, on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='materials',
        blank=True, null=True, on_delete=models.CASCADE,
    )
    date = models.DateTimeField('Date', default=timezone.now)
    draft = models.BooleanField('Draft', default=True)
    storage = models.FileField(
        'Storage', upload_to=get_storage_filename, blank=True
    )
    storage_name = models.CharField('Storage name', max_length=50)
    image = models.ImageField(
        'Original image', upload_to=get_image_filename, blank=True
    )
    thumb_big = models.ImageField(
        'Preview (Big)', upload_to=get_image_filename, blank=True
    )
    thumb_medium = models.ImageField(
        'Preview (Medium)', upload_to=get_image_filename, blank=True
    )
    thumb_small = models.ImageField(
        'Preview (Small)', upload_to=get_image_filename, blank=True
    )
    downloads = models.IntegerField('Number of downloads', default=0)
    rating = models.FloatField('Rating', default=0)
    votes_count = models.IntegerField('Number of votes', default=0)

    @property
    def html_description(self):
        return self.description

    @property
    def text_description(self):
        return html2text.html2text(self.description)

    objects = MaterialManager()

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materials'
        ordering = ['-date']

    def __str__(self):
        return '{category} - {name}'.format(
            category=self.category,
            name=self.name,
        )

    def get_absolute_url(self):
        return reverse('materials:detail', kwargs={
            'pk': self.pk,
            'slug': self.slug,
        })

    def get_download_url(self):
        return reverse('materials:download', kwargs={
            'pk': self.pk,
            'slug': self.slug,
        })

    def update_downloads(self):
        self.downloads = self.statistics.aggregate(
            models.Sum('count')
        )['count__sum'] or 0
        self.save()

    def update_rating(self):
        self.rating = self.votes.aggregate(
            models.Avg('score')
        )['score__avg'] or 0
        self.rating = round(self.rating, 2)
        self.votes_count = self.votes.count()
        self.save()

    def voted_users(self):
        return self.votes.values_list('user', flat=True)

    def favorited_users(self):
        return self.favorites.values_list('user', flat=True)

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Material, self).save(**kwargs)

    def make_thumbs(self):
        tmp = tempfile.mktemp(suffix='.jpg')
        pil_image = Image.open(self.image.path)
        pil_image.thumbnail((1024, 1024))
        pil_image.save(tmp)
        with open(tmp, 'rb') as f:
            self.thumb_big.save('tmp.jpg', ContentFile(f.read()))
        pil_image.thumbnail((512, 512))
        pil_image.save(tmp)
        with open(tmp, 'rb') as f:
            self.thumb_medium.save('tmp.jpg', ContentFile(f.read()))
        pil_image.thumbnail((256, 256))
        pil_image.save(tmp)
        with open(tmp, 'rb') as f:
            self.thumb_small.save('tmp.jpg', ContentFile(f.read()))

    def send_comment_notification(self):
        if self.user.profile.send_notifications:
            send_templated_mail(
                '[Blendermada] Somebody comment on {}'.format(self.name),
                'materials/comment_notification.txt',
                {'material': self},
                [self.user.email],
            )


class Statistic(models.Model):

    material = models.ForeignKey(
        Material, related_name='statistics', on_delete=models.CASCADE)
    date = models.DateField('Date', default=timezone.now)
    count = models.IntegerField('Count', default=1)

    class Meta:
        verbose_name = 'Statistic'
        verbose_name_plural = 'Statistics'
        ordering = ['-date', '-count']

    def __str__(self):
        return '{date} - {material}'.format(date=self.date, material=self.material)


class Vote(models.Model):

    material = models.ForeignKey(
        Material, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='votes', on_delete=models.CASCADE)
    score = models.PositiveIntegerField('Score')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
        ordering = ['-modified_at']
        unique_together = ('material', 'user')

    def __str__(self):
        return '{user} - {material}'.format(user=self.user, material=self.material)
