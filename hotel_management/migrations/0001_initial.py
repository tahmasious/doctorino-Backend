# Generated by Django 4.1.2 on 2022-11-30 16:37

from django.db import migrations, models
import django.db.models.deletion
import hotel_management.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade_code', models.CharField(blank=True, max_length=256, null=True)),
                ('hotel_name', models.CharField(max_length=256, null=True)),
                ('hotel_stars', models.SmallIntegerField(null=True)),
                ('hotel_description', models.CharField(blank=True, max_length=1024, null=True)),
                ('address', models.CharField(max_length=256, null=True)),
                ('cover_image', models.ImageField(blank=True, default=hotel_management.models.get_default_hotel_image_cover, null=True, upload_to='hotel-images')),
                ('rules', models.CharField(blank=True, max_length=256, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('features', models.ManyToManyField(blank=True, null=True, related_name='features', to='hotel_management.feature')),
                ('hotel_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel', to='authentication.hotelowner')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=1)),
                ('bed_count', models.SmallIntegerField(blank=True, default=1)),
                ('price_per_night', models.PositiveIntegerField(null=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel_management.hotel')),
            ],
        ),
        migrations.CreateModel(
            name='RoomImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='room-images')),
                ('is_thumbnail', models.BooleanField(blank=True, default=False, null=True)),
                ('is_cover', models.BooleanField(blank=True, default=False, null=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel_management.room')),
            ],
        ),
    ]
