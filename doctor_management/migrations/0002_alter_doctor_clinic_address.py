# Generated by Django 4.1.2 on 2022-11-24 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='clinic_address',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]