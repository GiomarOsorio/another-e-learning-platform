# Generated by Django 3.0.6 on 2020-06-12 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0011_auto_20200611_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examuserrelations',
            name='lastTry',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]