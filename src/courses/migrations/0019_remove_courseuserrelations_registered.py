# Generated by Django 3.0.6 on 2020-06-07 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0018_auto_20200607_0850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseuserrelations',
            name='registered',
        ),
    ]
