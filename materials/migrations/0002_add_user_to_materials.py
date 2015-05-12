from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('materials', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='user',
            field=models.ForeignKey(related_name='materials', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='material',
            name='author',
            field=models.ForeignKey(related_name='materials', blank=True, to='materials.Author', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='material',
            name='engine',
            field=models.CharField(max_length=3, verbose_name=b'Render engine', choices=[(b'int', b'Blender Internal'), (b'cyc', b'Cycles'), (b'lux', b'Lux Render'), (b'yfr', b'YafaRay'), (b'oct', b'Octane'), (b'nox', b'NOX Render')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='material',
            name='name',
            field=models.CharField(max_length=20, verbose_name=b'Name'),
            preserve_default=True,
        ),
    ]
