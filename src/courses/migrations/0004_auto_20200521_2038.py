# Generated by Django 3.0.6 on 2020-05-21 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20200518_2211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='learn',
        ),
        migrations.AddField(
            model_name='course',
            name='tags',
            field=models.TextField(default='', help_text='Required. to improve course searches', verbose_name='tags'),
        ),
        migrations.AddField(
            model_name='course',
            name='what_learn',
            field=models.TextField(default='', help_text='Required. describes what they learn with the course.', verbose_name='what will you learn'),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(help_text='Required. 500 characters or fewer.', max_length=500, verbose_name='course description'),
        ),
    ]
