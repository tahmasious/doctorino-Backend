# Generated by Django 4.1.2 on 2022-11-28 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_management', '0003_doctor_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='education',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='office_number',
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='phone_number',
            field=models.CharField(max_length=11, null=True),
        ),
    ]
