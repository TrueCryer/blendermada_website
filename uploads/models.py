from __future__ import unicode_literals

from uuid import uuid4
from os import path

from django.core.files import File
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

from core.mail import send_templated_mail
from materials.models import Material, Category


def get_upload_filename(instance, filename):
    ext = path.splitext(filename)[1]
    return path.join('userfiles', instance.date.strftime('%Y-%m-%d'), '{name}{ext}'.format(name=uuid4(), ext=ext))


def get_rendered_filename(instance, filename):
    ext = path.splitext(filename)[1]
    return path.join('rendered', instance.date.strftime('%Y-%m-%d'), '{name}{ext}'.format(name=uuid4(), ext=ext))


ENGINE_VERSIONS = (
    ('cyc272', 'Cycles 2.72'),
    ('int272', 'Internal 2.72'),
)

PROCESS_STATUSES = (
    ('w', 'Pending'),
    ('r', 'Rendering'),
    ('a', 'Approving'),
    ('p', 'Publishing'),
    ('d', 'Deleting'),
    ('e', 'Error'),
)

CSS_STATUS_MAPPING = {
    'w': '',
    'r': 'active',
    'a': 'warning',
    'p': 'success',
    'd': 'info',
    'e': 'danger',
}

SCENE_TYPES = (
    ('s', 'Solid'),
    ('c', 'Cloth'),
    ('u', 'UV unwrapped'),
    ('f', '(Not Implemented) Fluid'),
    ('v', '(Not Implemented) Volume'),
    ('e', 'Emission'),
)


class UploadManager(models.Manager):
    def pop_next_to_render(self):
        try:
            next_to_render = self.filter(status='w')[0]
        except IndexError:
            raise Upload.DoesNotExist
        next_to_render.status = 'r'
        next_to_render.render_started = timezone.now()
        next_to_render.save()
        return next_to_render


@python_2_unicode_compatible
class Upload(models.Model):
    name = models.CharField('Name', max_length=20)
    description = models.TextField('Description', blank=True)
    uploaded_file = models.FileField('Uploaded file', upload_to=get_upload_filename)
    name_in_file = models.CharField('Material name in file', max_length=50)
    engine = models.CharField('Engine version', max_length=6, choices=ENGINE_VERSIONS)
    scene = models.CharField('Scene type', max_length=1, choices=SCENE_TYPES)

    date = models.DateTimeField('Upload date', default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='uploads', blank=True, null=True)
    status = models.CharField('Status', max_length=1, choices=PROCESS_STATUSES, default='w')
    render_started = models.DateTimeField('Render started at', blank=True, null=True)
    render_finished = models.DateTimeField('Render finished at', blank=True, null=True)
    error = models.TextField('Error description', blank=True)

    storage = models.FileField('Storage', upload_to=get_rendered_filename, blank=True)
    image = models.ImageField('Rendered image', upload_to=get_rendered_filename, blank=True)

    category = models.ForeignKey(Category, related_name='uploads', blank=True, null=True)
    user_approved = models.BooleanField('Approved by user', default=False)
    admin_approved = models.BooleanField('Approved by admin', default=False)

    objects = UploadManager()

    class Meta:
        verbose_name = 'Upload'
        verbose_name_plural = 'Uploads'
        ordering = ['date']

    def __str__(self):
        return '{name} by {author}, {date}'.format(name=self.name, author=self.author, date=self.date.strftime('%Y-%m-%d %H:%M:%S'))

    @models.permalink
    def get_absolute_url(self):
        return ('uploads_detail', [], {'pk':self.pk})

    def get_css_class(self):
        return CSS_STATUS_MAPPING[self.status]

    def rendered(self):
        return self.status in ('a', 'p', 'd')

    def mail_about_ready(self):
        if self.status == 'e':
            send_templated_mail(
                'Material isn\'t rendered because of error',
                'uploads/error_mail.txt',
                {'upload': self},
                [self.author.email],
            )
        else:
            send_templated_mail(
                'Material is rendered and ready',
                'uploads/ready_mail.txt',
                {'upload': self},
                [self.author.email],
            )

    def publish(self):
        material = Material()
        material.name = self.name
        material.user = self.author
        material.category = self.category
        material.date = timezone.now()
        material.description = self.description
        material.engine = self.engine[:3]
        material.draft = False
        material.storage = File(self.storage, self.storage.name)
        material.storage_name = self.name_in_file
        material.image = File(self.image, self.image.name)
        material.save()
        material.make_thumbs()
        self.status = 'd'
        self.save()


@python_2_unicode_compatible
class Scene(models.Model):

    engine = models.CharField('Engine version', max_length=6, choices=ENGINE_VERSIONS)
    type = models.CharField('Scene type', max_length=1, choices=SCENE_TYPES)
    description = models.TextField('Description', blank=True)
    file = models.FileField('Scene file', upload_to='uploads/scenes/', blank=True)
    image = models.ImageField('Original image', upload_to='uploads/scenes/', blank=True)
    thumb_big = models.ImageField('Thumbnail (big)', upload_to='uploads/scenes/', blank=True)
    thumb_small = models.ImageField('Thumbnail (small)', upload_to='uploads/scenes/', blank=True)

    class Meta:
        verbose_name = 'Scene'
        verbose_name_plural = 'Scenes'
        ordering = ['engine']

    def __str__(self):
        return '{engine} - {scene}'.format(engine=self.get_engine_display(), scene=self.get_type_display())
