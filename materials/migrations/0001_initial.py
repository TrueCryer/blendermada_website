from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'Name')),
                ('email', models.EmailField(max_length=50, verbose_name=b'E-mail')),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25, verbose_name=b'Name')),
                ('slug', models.SlugField(verbose_name=b'Slug')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('engine', models.CharField(max_length=3, verbose_name=b'Render engine', choices=[(b'int', b'BLENDER INTERNAL'), (b'cyc', b'CYCLES'), (b'lux', b'LUX RENDER'), (b'yfr', b'YAFARAY'), (b'oct', b'OCTANE'), (b'nox', b'NOX RENDER')])),
                ('name', models.CharField(max_length=25, verbose_name=b'Name')),
                ('slug', models.SlugField(verbose_name=b'Slug')),
                ('description', models.TextField(verbose_name=b'Description', blank=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Date')),
                ('draft', models.BooleanField(default=True, verbose_name=b'Draft')),
                ('storage', models.FileField(upload_to=b'materials/storage/', verbose_name=b'Storage', blank=True)),
                ('storage_name', models.CharField(max_length=50, verbose_name=b'Storage name')),
                ('image_big', models.ImageField(upload_to=b'materials/preview/big/', verbose_name=b'Preview (Big)', blank=True)),
                ('image_medium', models.ImageField(upload_to=b'materials/preview/medium/', verbose_name=b'Preview (Medium)', blank=True)),
                ('image_small', models.ImageField(upload_to=b'materials/preview/small/', verbose_name=b'Preview (Small)', blank=True)),
                ('downloads', models.IntegerField(default=0, verbose_name=b'Number of downloads')),
                ('author', models.ForeignKey(related_name='materials', to='materials.Author')),
                ('category', models.ForeignKey(related_name='materials', to='materials.Category')),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'Material',
                'verbose_name_plural': 'Materials',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name=b'Date')),
                ('count', models.IntegerField(default=1, verbose_name=b'Count')),
                ('material', models.ForeignKey(related_name='statistics', to='materials.Material')),
            ],
            options={
                'ordering': ['-date', '-count'],
                'verbose_name': 'Statistic',
                'verbose_name_plural': 'Statistics',
            },
            bases=(models.Model,),
        ),
    ]
