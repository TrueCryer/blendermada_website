# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('mailing_type', models.CharField(choices=[('adm', 'ADMINS'), ('mod', 'MODERATORS'), ('aut', 'AUTHORS'), ('sub', 'SUBSCRIBERS'), ('all', 'ALL')], verbose_name='Mailing type', max_length=3)),
                ('subject', models.CharField(verbose_name='Subject', max_length=255)),
                ('message', models.TextField(verbose_name='Template')),
            ],
            options={
                'verbose_name_plural': 'Mails',
                'verbose_name': 'Mail'
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('host', models.CharField(verbose_name='Host', max_length=255)),
                ('port', models.IntegerField(verbose_name='Port')),
                ('username', models.CharField(verbose_name='Username', max_length=255)),
                ('password', models.CharField(verbose_name='Password', max_length=255)),
                ('use_tls', models.BooleanField(default=False, verbose_name='Use TLS')),
                ('use_ssl', models.BooleanField(default=False, verbose_name='Use SSL')),
                ('timeout', models.IntegerField(default=30, verbose_name='Timeout')),
                ('sender', models.CharField(verbose_name='Sender', max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Settings',
                'verbose_name': 'Setting'
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='mail',
            name='setting',
            field=models.ForeignKey(to='mailing.Setting'),
            preserve_default=True,
        ),
    ]
