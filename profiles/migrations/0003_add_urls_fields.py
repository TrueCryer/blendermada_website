# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_add_show_email_fullname_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='about',
            field=models.TextField(verbose_name='About', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='deviantart',
            field=models.CharField(verbose_name='Deviantart', max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='facebook',
            field=models.CharField(verbose_name='Facebook', max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='gplus',
            field=models.CharField(verbose_name='Google+', max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='twitter',
            field=models.CharField(verbose_name='Twitter', max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='website',
            field=models.CharField(verbose_name='Website', max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
