# Generated by Django 3.2.25 on 2024-12-14 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20241214_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onetimeevent',
            name='event_history',
            field=models.TextField(default='N/AA'),
        ),
    ]