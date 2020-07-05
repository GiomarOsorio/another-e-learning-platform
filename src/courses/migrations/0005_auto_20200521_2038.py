# Generated by Django 3.0.6 on 2020-05-21 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20200521_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='tags',
            field=models.TextField(help_text='Required. to improve course searches', verbose_name='tags'),
        ),
        migrations.AlterField(
            model_name='course',
            name='what_learn',
            field=models.TextField(help_text='Required. describes what they learn with the course.', verbose_name='what will you learn'),
        ),
    ]
