# Generated by Django 4.1.2 on 2022-12-05 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_management', '0003_workdayperiod'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='description',
            field=models.TextField(blank=True, max_length=7000, null=True),
        ),
    ]