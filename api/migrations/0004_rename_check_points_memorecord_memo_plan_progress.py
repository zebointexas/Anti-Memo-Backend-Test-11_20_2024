# Generated by Django 3.2.25 on 2024-12-02 01:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20241130_2349'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memorecord',
            old_name='Check_Points',
            new_name='memo_plan_progress',
        ),
    ]