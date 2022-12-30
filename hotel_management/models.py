from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from authentication.models import User, HotelOwner
from django.core.exceptions import ValidationError
from django_jalali.db import models as jmodels
from django.contrib.gis.db import models as lcmodels
from django.contrib.gis.geos import Point
from utils.cons import PROVINCE_CHOICES, CITY_CHOICES


def get_default_hotel_image_cover():
    return 'hotel-images/default_hotel_image.jpg'


class Feature(models.Model):
    title = models.CharField(max_length=256, null=True)

    def __str__(self):
        return self.title


class Hotel(models.Model):
    hotel_owner = models.ForeignKey(HotelOwner, on_delete=models.CASCADE, related_name='hotel')
    trade_code = models.CharField(max_length=256, null=True, blank=True)
    hotel_name = models.CharField(max_length=256, null=True)
    hotel_stars = models.SmallIntegerField(null=True)
    hotel_description = models.CharField(max_length=1024, blank=True, null=True)
    address = models.CharField(max_length=256, null=True)
    cover_image = models.ImageField(upload_to='hotel-images', null=True, blank=True, default=get_default_hotel_image_cover)
    rules = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    features = models.ManyToManyField(Feature, related_name="features", blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=False, null=True)
    province = models.IntegerField(choices=PROVINCE_CHOICES, blank=False, null=True, default=0)
    city = models.IntegerField(choices=CITY_CHOICES, blank=False, null=True, default=0)
    location = lcmodels.PointField(geography=True, default=Point(0.0, 0.0))

    def __str__(self):
        return self.hotel_name

    @property
    def rate(self):
        query = HotelReview.objects.filter(hotel=self)
        if not query.exists():
            return 0
        count = len(query)
        sum = 0
        for review in query:
            sum += review.score
        return round(float(sum / count), 2)


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel')
    quantity = models.IntegerField(default=1, blank=True)
    bed_count = models.SmallIntegerField(default=1, blank=True)
    price_per_night = models.PositiveIntegerField(null=True)
    room_title = models.CharField(max_length=300, blank=True, null=True)



class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room-images', blank=False, null=True)
    is_thumbnail = models.BooleanField(default=False, blank=True, null=True)
    is_cover = models.BooleanField(default=False, blank=True, null=True)


class HotelReservation(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel_room = models.ForeignKey(Room, on_delete=models.CASCADE)
    from_date = jmodels.jDateField()
    to_date = jmodels.jDateField()

class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel-image', blank=True, null=True)


class HotelReview(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField(null=True, blank=True)
