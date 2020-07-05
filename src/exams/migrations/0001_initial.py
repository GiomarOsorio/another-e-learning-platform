# Generated by Django 3.0.6 on 2020-05-31 01:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0012_auto_20200531_0118'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required. 150 characters or fewer.', max_length=150, verbose_name='quiz name')),
                ('description', models.TextField()),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('content', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.Content')),
                ('course', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
                ('module', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.Module')),
                ('segment', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.Segment')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(error_messages={'unique': 'A question with that name already exists.'}, help_text='Required. 300 characters or fewer.', max_length=600, verbose_name='question')),
                ('correct_answers', models.IntegerField(default=0, help_text='number of correct answers for this question', verbose_name='number of correct answers for this question')),
                ('quiz', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='exams.Exam')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=600, verbose_name='answer')),
                ('correct_answer', models.BooleanField(default=False, help_text='the answer is correct?.')),
                ('question', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='exams.Question')),
                ('quiz', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='exams.Exam')),
            ],
        ),
    ]
