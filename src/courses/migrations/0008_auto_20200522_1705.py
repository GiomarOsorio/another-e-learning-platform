# Generated by Django 3.0.6 on 2020-05-22 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_content_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='name',
            field=models.CharField(help_text='Required. 120 characters or fewer.', max_length=120, verbose_name='segment name'),
        ),
    ]