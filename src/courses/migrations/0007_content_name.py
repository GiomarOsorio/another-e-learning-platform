# Generated by Django 3.0.6 on 2020-05-22 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20200521_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='name',
            field=models.CharField(default='', help_text='Required. 120 characters or fewer.', max_length=120, verbose_name='segment name'),
        ),
    ]
