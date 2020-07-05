# Generated by Django 3.0.6 on 2020-05-21 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='academic_degree',
            field=models.CharField(blank=True, default='', error_messages={'null': 'you must select your academic degree.'}, max_length=70, verbose_name='academic degree'),
        ),
        migrations.AddField(
            model_name='user',
            name='github',
            field=models.CharField(blank=True, default='', max_length=70, null=True, verbose_name='github'),
        ),
        migrations.AddField(
            model_name='user',
            name='linkedin',
            field=models.CharField(blank=True, default='', max_length=70, null=True, verbose_name='linkedin'),
        ),
    ]
