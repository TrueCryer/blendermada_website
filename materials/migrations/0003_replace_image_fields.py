# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import materials.models


def translate_image_fields(apps, schema_editor):
    Material = apps.get_model('materials', 'Material')
    db_alias = schema_editor.connection.alias
    for mat in Material.objects.using(db_alias).all():
        mat.thumb_big = mat.image_big
        mat.thumb_medium = mat.image_medium
        mat.thumb_small = mat.image_small
        mat.save()

class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_add_user_to_materials'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='storage',
            field=models.FileField(upload_to=materials.models.get_storage_filename, verbose_name='Storage', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='material',
            name='image',
            field=models.ImageField(upload_to=materials.models.get_image_filename, verbose_name='Original image', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='material',
            name='thumb_big',
            field=models.ImageField(upload_to=materials.models.get_image_filename, verbose_name='Preview (Big)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='material',
            name='thumb_medium',
            field=models.ImageField(upload_to=materials.models.get_image_filename, verbose_name='Preview (Medium)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='material',
            name='thumb_small',
            field=models.ImageField(upload_to=materials.models.get_image_filename, verbose_name='Preview (Small)', blank=True),
            preserve_default=True,
        ),
        migrations.RunPython(
            translate_image_fields,
        ),
        migrations.RemoveField(
            model_name='material',
            name='image_big',
        ),
        migrations.RemoveField(
            model_name='material',
            name='image_medium',
        ),
        migrations.RemoveField(
            model_name='material',
            name='image_small',
        ),
    ]
