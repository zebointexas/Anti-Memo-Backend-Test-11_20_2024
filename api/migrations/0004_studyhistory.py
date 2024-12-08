# Generated by Django 3.2.25 on 2024-12-05 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_memorecord_study_plan'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('study_history', models.TextField()),
                ('today_study_count', models.SmallIntegerField(default=1)),
                ('record_details_change_history', models.TextField()),
            ],
        ),
    ]
