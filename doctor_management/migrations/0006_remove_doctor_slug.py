# Generated by Django 4.1.2 on 2022-11-30 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_management', '0005_doctor_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='slug',
        ),
    ]
