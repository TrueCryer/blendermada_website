from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import uploads.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name=b'Name')),
                ('description', models.TextField(verbose_name=b'Description', blank=True)),
                ('uploaded_file', models.FileField(upload_to=uploads.models.get_upload_filename, verbose_name=b'Uploaded file')),
                ('name_in_file', models.CharField(max_length=50, verbose_name=b'Material name in file')),
                ('engine', models.CharField(max_length=6, verbose_name=b'Engine version', choices=[(b'cyc272', b'Cycles 2.72'), ('int272', 'Internal 2.72')])),
                ('scene', models.CharField(max_length=1, verbose_name=b'Scene type', choices=[(b's', b'Solid'), (b'c', b'Cloth'), (b'u', b'UV unwrapped'), (b'f', b'Fluid'), (b'v', b'Volume'), (b'e', b'Emission')])),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Date')),
                ('author', models.ForeignKey(related_name='uploads', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('status', models.CharField(default=b'w', max_length=1, verbose_name=b'Status', choices=[(b'w', b'Pending'), (b'r', b'Rendering'), (b'a', b'Approving'), (b'p', b'Publishing'), (b'd', b'Deleting'), (b'e', b'Error')])),
                ('render_started', models.DateTimeField(null=True, verbose_name=b'Render started at', blank=True)),
                ('render_finished', models.DateTimeField(null=True, verbose_name=b'Render finished at', blank=True)),
                ('storage', models.FileField(upload_to=uploads.models.get_rendered_filename, verbose_name=b'Storage', blank=True)),
                ('image', models.ImageField(upload_to=uploads.models.get_rendered_filename, verbose_name=b'Rendered image', blank=True)),
                ('user_approved', models.BooleanField(default=False, verbose_name=b'Approved by user')),
                ('admin_approved', models.BooleanField(default=False, verbose_name=b'Approved by admin')),
            ],
            options={
                'ordering': ['date'],
                'verbose_name': 'Upload',
                'verbose_name_plural': 'Uploads',
            },
            bases=(models.Model,),
        ),
    ]
