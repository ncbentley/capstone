# Generated by Django 3.0.8 on 2020-07-13 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_sprint_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sprint',
            name='completed',
        ),
    ]
