# Generated by Django 3.2.25 on 2024-12-02 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20241202_0130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memorecord',
            name='record_Id',
        ),
        migrations.AddField(
            model_name='memorecord',
            name='id',
            field=models.AutoField(primary_key=True, default=None),
            preserve_default=False,
        ),
    ]