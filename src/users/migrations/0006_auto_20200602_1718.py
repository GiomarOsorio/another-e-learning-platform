# Generated by Django 3.0.6 on 2020-06-02 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200602_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='university',
            field=models.CharField(blank=True, error_messages={'null': 'you must enter your University.'}, max_length=70, verbose_name='university'),
        ),
    ]
