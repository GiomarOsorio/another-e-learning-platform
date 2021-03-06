# Generated by Django 3.0.6 on 2020-05-27 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_auto_20200522_1937'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='segments',
        ),
        migrations.AlterField(
            model_name='content',
            name='course',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.Course'),
        ),
        migrations.AlterField(
            model_name='content',
            name='module',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.Module'),
        ),
        migrations.AlterField(
            model_name='content',
            name='segment',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.Segment'),
        ),
        migrations.AlterField(
            model_name='module',
            name='course',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.Course'),
        ),
        migrations.AlterField(
            model_name='segment',
            name='course',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.Course'),
        ),
        migrations.AlterField(
            model_name='segment',
            name='module',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.Module'),
        ),
    ]
