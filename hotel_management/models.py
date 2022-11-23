from django.db import models
from authentication.models import User, HotelOwner


class Feature(models.Model):
    title = models.CharField(max_length=256, null=True)

    def __str__(self):
        return self.title


class Hotel(models.Model):
    hotel_owner = models.OneToOneField(HotelOwner, on_delete=models.CASCADE, related_name='hotel')
    trade_code = models.CharField(max_length=256, null=True, blank=True)
    hotel_name = models.CharField(max_length=256, null=True)
    hotel_stars = models.SmallIntegerField(null=True)
    hotel_description = models.CharField(max_length=1024, blank=True, null=True)
    address = models.CharField(max_length=256, null=True)
    rules = models.CharField(max_length=256, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    features = models.ManyToManyField(Feature, related_name="features", blank=True, null=True)

    def __str__(self):
        return self.hotel_name


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, blank=True)
    bed_count = models.SmallIntegerField(default=1, blank=True)
    price_per_night = models.PositiveIntegerField(null=True)


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room-images', blank=True, null=True)
    is_thumbnail = models.BooleanField(default=False, blank=True, null=True)
    is_cover = models.BooleanField(default=False, blank=True, null=True)


