# Generated by Django 3.0.6 on 2020-05-22 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200522_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='academic_degree',
            field=models.CharField(blank=True, error_messages={'null': 'you must select your academic degree.'}, max_length=70, verbose_name='academic degree'),
        ),
        migrations.AlterField(
            model_name='user',
            name='twitter',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='linkedin'),
        ),
    ]
