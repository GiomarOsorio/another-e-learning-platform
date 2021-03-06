# Generated by Django 3.0.6 on 2020-06-18 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20200618_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user is a platform staff.', verbose_name='staff'),
        ),
    ]
