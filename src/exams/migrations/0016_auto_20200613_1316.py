# Generated by Django 3.0.6 on 2020-06-13 13:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0015_auto_20200613_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examuserrelations',
            name='points',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]