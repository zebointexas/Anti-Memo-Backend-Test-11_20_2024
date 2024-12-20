# Generated by Django 3.2.25 on 2024-12-09 20:50

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OneTimeEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_Id', models.SmallIntegerField()),
                ('event_details', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('retain_length', models.SmallIntegerField()),
                ('is_done', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='StudyHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('study_history', models.TextField()),
                ('study_days_count', models.SmallIntegerField(default=1)),
                ('record_details_change_history', models.TextField(default='')),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudyPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soft_reset_date', models.DateTimeField(auto_now_add=True)),
                ('check_points', models.JSONField(default=api.models.get_default_check_points)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MemoRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_type', models.CharField(max_length=20)),
                ('importance_level', models.SmallIntegerField(default=1)),
                ('in_half_year_repetition', models.BooleanField(default=False)),
                ('record_details', models.TextField()),
                ('record_neighbor', models.CharField(default='N/A', max_length=100)),
                ('next_study_time', models.DateTimeField(auto_now_add=True)),
                ('is_activate', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='memo_records', to=settings.AUTH_USER_MODEL)),
                ('study_history_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='study_history_model', to='api.studyhistory')),
                ('study_plan_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='study_plan_model', to='api.studyplan')),
            ],
        ),
    ]
