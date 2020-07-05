# Generated by Django 3.0.6 on 2020-06-04 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200604_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='media/default.png', help_text='maxime zise of 1MB. JPG ó PNG.', upload_to='media/avatar_pics/', verbose_name='Avatar image'),
        ),
    ]
