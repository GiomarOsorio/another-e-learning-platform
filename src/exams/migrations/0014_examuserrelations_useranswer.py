# Generated by Django 3.0.6 on 2020-06-13 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0013_auto_20200612_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='examuserrelations',
            name='userAnswer',
            field=models.CharField(blank=True, default=None, max_length=600, null=True),
        ),
    ]