# Generated by Django 3.2.25 on 2024-12-18 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='blog_type',
            field=models.CharField(default='Personal', max_length=20),
            preserve_default=False,
        ),
    ]
