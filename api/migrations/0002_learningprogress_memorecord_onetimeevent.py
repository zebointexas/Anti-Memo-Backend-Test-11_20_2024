# Generated by Django 3.2.25 on 2024-11-29 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearningProgress',
            fields=[
                ('progress_id', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('nominal_start_date', models.DateTimeField()),
                ('Check_Points', models.TextField(default=' Day_1: false\n                    Day_1_repeat: false\n                    Day_2: false\n                    Day_4: false\n                    Day_8: false\n                    Day_15: false\n                    Day_30: false\n                    Day_60: false\n                    Day_90: false\n                    Day_120: false\n                    Day_180: false\n                    Day_300: false\n                    Day_480: false\n                    Day_640: false\n                    Day_End: false\n                ')),
                ('in_half_year_repetition', models.BooleanField()),
            ],
        ),
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
            name='MemoRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_Id', models.SmallIntegerField()),
                ('subject_Type', models.CharField(choices=[('Java', 'Java'), ('Python', 'Python'), ('Algo', 'Algo'), ('System_Design', 'System_Design'), ('ODD', 'OOD'), ('Linux', 'Linux'), ('Network', 'Network'), ('General_IT', 'General_IT'), ('BQ', 'BQ'), ('French', 'French'), ('English', 'English'), ('Friends_Info', 'Friends_Info'), ('Math', 'Math'), ('Machine_Learning', 'Machine_Learning')], default='Algo', max_length=20)),
                ('importance_Level', models.SmallIntegerField()),
                ('memo_History', models.TextField()),
                ('record_Details', models.TextField()),
                ('recordNeighbor', models.CharField(max_length=100)),
                ('Learning_Progress_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memo_record', to='api.learningprogress')),
            ],
        ),
    ]