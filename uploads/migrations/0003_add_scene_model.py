# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0002_add_category_and_error'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scene',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('engine', models.CharField(max_length=6, verbose_name='Engine version', choices=[('cyc272', 'Cycles 2.72'), ('int272', 'Internal 2.72')])),
                ('type', models.CharField(max_length=1, verbose_name='Scene type', choices=[('s', 'Solid'), ('c', 'Cloth'), ('u', 'UV unwrapped'), ('f', 'Fluid'), ('v', 'Volume'), ('e', 'Emission')])),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('file', models.FileField(upload_to='uploads/scenes/', verbose_name='Scene file', blank=True)),
                ('image', models.ImageField(upload_to='uploads/scenes/', verbose_name='Original image', blank=True)),
                ('thumb_big', models.ImageField(upload_to='uploads/scenes/', verbose_name='Thumbnail (big)', blank=True)),
                ('thumb_small', models.ImageField(upload_to='uploads/scenes/', verbose_name='Thumbnail (small)', blank=True)),
            ],
            options={
                'ordering': ['engine'],
                'verbose_name': 'Scene',
                'verbose_name_plural': 'Scenes',
            },
            bases=(models.Model,),
        ),
    ]
