# Generated by Django 3.0.6 on 2020-06-04 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_auto_20200603_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='banner',
            field=models.ImageField(default='media/defaultbanner.png', help_text='maxime zise of 2MB. JPG ó PNG.', upload_to='media/banner_pics/', verbose_name='banner image'),
        ),
    ]