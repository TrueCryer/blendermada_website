# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=100)),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'verbose_name': 'category',
                'ordering': ('title',),
                'db_table': 'blog_categories',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=200)),
                ('slug', models.SlugField(verbose_name='slug', unique_for_date='publish')),
                ('body', models.TextField(verbose_name='body')),
                ('tease', models.TextField(verbose_name='tease', help_text='Concise text suggested. Does not appear in RSS feed.', blank=True)),
                ('status', models.CharField(verbose_name='status', default='d', max_length=2, choices=[('d', 'Draft'), ('p', 'Public')])),
                ('allow_comments', models.BooleanField(verbose_name='allow comments', default=True)),
                ('publish', models.DateTimeField(verbose_name='publish', default=django.utils.timezone.now)),
                ('created', models.DateTimeField(verbose_name='created', auto_now_add=True)),
                ('modified', models.DateTimeField(verbose_name='modified', auto_now=True)),
                ('author', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='posts', blank=True)),
                ('categories', models.ManyToManyField(blank=True, to='blog.Category', related_name='posts')),
            ],
            options={
                'verbose_name_plural': 'posts',
                'verbose_name': 'post',
                'ordering': ('-publish',),
                'get_latest_by': 'publish',
            },
        ),
    ]
