# Generated by Django 4.2.20 on 2025-04-22 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20250307_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='memorecord',
            name='current_Learning_Session',
            field=models.BooleanField(default=False),
        ),
    ]
