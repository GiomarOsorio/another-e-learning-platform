# Generated by Django 3.0.6 on 2020-06-25 01:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0021_auto_20200618_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_value',
            field=models.DecimalField(decimal_places=2, default=None, error_messages={'blank': 'you must provied the point value.', 'null': 'you must provied the point value.'}, help_text='Max 5 digits: same as "minimun points to approved"', max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='points'),
        ),
    ]