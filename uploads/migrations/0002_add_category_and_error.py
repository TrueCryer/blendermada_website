from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0001_initial'),
        ('uploads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='category',
            field=models.ForeignKey(related_name='uploads', blank=True, to='materials.Category', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='upload',
            name='error',
            field=models.TextField(verbose_name='Error description', blank=True),
            preserve_default=True,
        ),
    ]
