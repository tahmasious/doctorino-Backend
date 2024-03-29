from django.db import models
from django.contrib.auth.models import AbstractUser
from django_jalali.db import models as jmodels
from utils.cons import PROVINCE_CHOICES, CITY_CHOICES


class User(AbstractUser):
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female'),
        (2, 'not specified'),
    )

    username = models.CharField(max_length=120, unique=True, blank=False, null=True)
    is_hotel_owner = models.BooleanField(default=False, blank=True, null=True)
    is_doctor = models.BooleanField(default=False, blank=True, null=True)
    email = models.EmailField(unique=True, blank=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class HotelOwner(models.Model):
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female'),
        (2, 'not specified'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner')
    shaba_code = models.CharField(max_length=256, null=True, blank=True)
    father_name = models.CharField(max_length=124, null=True, blank=False)
    national_code = models.CharField(max_length=10, unique=True, blank=False, null=True)
    social_number = models.CharField(max_length=20, blank=False, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=2)
    first_phone_number = models.CharField(max_length=12, blank=False, null=True)
    second_phone_number = models.CharField(max_length=12, blank=True, null=True)
    area_code = models.CharField(max_length=20, blank=True, null=True)
    telephone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    birth_day = jmodels.jDateField(blank=False, null=True)

    def __str__(self):
        return f"{self.user.email}"


class Patient(models.Model):
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female'),
        (2, 'not specified'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')
    gender = models.IntegerField(choices=GENDER_CHOICES, default=2)
    code_melli = models.CharField(max_length=10, unique=True, blank=False, null=True)
    phone_number = models.CharField(max_length=11, blank=False, null=True)
    birth_day = jmodels.jDateField(blank=False, null=True)
    city = models.IntegerField(choices=CITY_CHOICES, blank=False, null=True, default=0)
    province = models.IntegerField(choices=PROVINCE_CHOICES, blank=False, null=True, default=0)
    is_active = models.BooleanField(default=False)


class VerificationCode(models.Model):
    code = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_code')
    creation_datetime = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)