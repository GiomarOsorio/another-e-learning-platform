# Generated by Django 3.0.6 on 2020-06-10 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0019_remove_courseuserrelations_registered'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='banner',
            field=models.ImageField(default='default.png', help_text='maxime zise of 2MB. JPG ó PNG.', upload_to='banner_pics/', verbose_name='banner image'),
        ),
    ]