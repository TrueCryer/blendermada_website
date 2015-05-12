# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('materials', '0003_replace_image_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.PositiveIntegerField(verbose_name='Score')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('material', models.ForeignKey(related_name='votes', to='materials.Material')),
                ('user', models.ForeignKey(related_name='votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-modified_at'],
                'verbose_name': 'Vote',
                'verbose_name_plural': 'Votes',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('material', 'user')]),
        ),
        migrations.AddField(
            model_name='material',
            name='rating',
            field=models.FloatField(default=0, verbose_name='Rating'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='material',
            name='votes_count',
            field=models.IntegerField(default=0, verbose_name='Number of votes'),
            preserve_default=True,
        ),
    ]
