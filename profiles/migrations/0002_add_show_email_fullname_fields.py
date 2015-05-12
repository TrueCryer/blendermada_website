# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='show_email',
            field=models.BooleanField(default=False, verbose_name='Show e-mail on site'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='show_fullname',
            field=models.BooleanField(default=False, verbose_name='Show full name on site'),
            preserve_default=True,
        ),
    ]
