from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from authentication.models import User, HotelOwner
from django.core.exceptions import ValidationError
from django_jalali.db import models as jmodels
from django.core.exceptions import ValidationError

CITY_CHOICES = (
    (0,"تعیین نشده"),
    (1,"آذربایجان شرقی",),
    (2,"آذربایجان غربی",),
    (3,"اردبیل",),
    (4,"اصفهان",),
    (5,"البرز",),
    (6,"ایلام",),
    (7,"بوشهر",),
    (8,"تهران",),
    (9,"چهارمحال و بختیاری",),
    (10,"خراسان جنوبی",),
    (11,"خراسان رضوی",),
    (12,"خراسان شمالی",),
    (13,"خوزستان",),
    (14,"زنجان",),
    (15,"سمنان",),
    (16,"سیستان و بلوچستان",),
    (17,"فارس",),
    (18,"قزوین",),
    (19,"قم",),
    (20,"کردستان",),
    (21,"کرمان",),
    (22,"کرمانشاه",),
    (23,"کهگیلویه و بویراحمد",),
    (24,"گلستان",),
    (25,"لرستان",),
    (26,"گیلان",),
    (27,"مازندران",),
    (28,"مرکزی",),
    (29,"هرمزگان",),
    (30,"همدان",),
    (31,"یزد",)
)

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
    city = models.IntegerField(choices=CITY_CHOICES, blank=False, null=True, default=0)

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
    # occupied_count = models.IntegerField(default=0, blank=True)
    # is_active = is_active = models.BooleanField(default=True, blank=True, null=True)
    # features = models.ManyToManyField(Feature, related_name="features", blank=True, null=True)


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room-images', blank=True, null=True)
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
