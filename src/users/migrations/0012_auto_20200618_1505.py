# Generated by Django 3.0.6 on 2020-06-18 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20200610_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_teacher',
            field=models.BooleanField(default=False, help_text='Designates if the user is a teacher of the platform.', verbose_name='teacher'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user is a platform administrator.', verbose_name='admin'),
        ),
    ]