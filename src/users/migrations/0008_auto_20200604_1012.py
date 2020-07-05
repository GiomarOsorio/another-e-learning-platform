# Generated by Django 3.0.6 on 2020-06-04 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='default.png', upload_to='avatar_pics', verbose_name='Avatar image'),
        ),
    ]
