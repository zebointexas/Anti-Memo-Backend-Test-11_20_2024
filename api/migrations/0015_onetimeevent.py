# Generated by Django 3.2.25 on 2024-12-14 16:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0014_delete_onetimeevent'),
    ]

    operations = [
        migrations.CreateModel(
            name='OneTimeEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=20)),
                ('event_details', models.TextField(default='N/A')),
                ('start_date', models.DateTimeField()),
                ('is_very_important', models.BooleanField(default=False)),
                ('is_done', models.BooleanField(default=False)),
                ('event_history', models.TextField(default='N/A')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='one_time_event', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
