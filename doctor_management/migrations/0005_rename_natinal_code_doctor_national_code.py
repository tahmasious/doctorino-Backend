# Generated by Django 4.1.2 on 2022-11-23 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_management', '0004_rename_is_verifyed_doctor_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='natinal_code',
            new_name='national_code',
        ),
    ]