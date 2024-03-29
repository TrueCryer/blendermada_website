# Generated by Django 4.0 on 2022-02-16 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registrationprofile',
            options={'verbose_name': 'registration profile', 'verbose_name_plural': 'registration profiles'},
        ),
        migrations.AlterField(
            model_name='registrationprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='user'),
        ),
    ]
