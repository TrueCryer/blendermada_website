from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activation_key', models.CharField(max_length=40, verbose_name='Activation key')),
                ('user', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, unique=True, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Registration profile',
                'verbose_name_plural': 'Registration profiles',
            },
            bases=(models.Model,),
        ),
    ]
