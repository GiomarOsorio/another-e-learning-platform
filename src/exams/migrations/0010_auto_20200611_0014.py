# Generated by Django 3.0.6 on 2020-06-11 00:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0022_auto_20200610_2014'),
        ('exams', '0009_auto_20200611_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='content',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.Content'),
        ),
    ]