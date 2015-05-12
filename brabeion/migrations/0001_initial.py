# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BadgeAward',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('awarded_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('slug', models.CharField(max_length=255)),
                ('level', models.IntegerField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='badges_earned')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
