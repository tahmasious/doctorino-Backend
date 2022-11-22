from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=120, unique=True, blank=False, null=True)
    is_hotel_owner = models.BooleanField(default=False, blank=True, null=True)
    is_doctor = models.BooleanField(default=False, blank=True, null=True)


# class Hotel(models.Model):
#     owner = models.ForeignKey(HotelOwner, on_delete=models.SET_NULL,related_name='hotel')
#     name = models.CharField(max_length=256, null=True, blank=True)
#     star = models.SmallIntegerField()


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hospital_owner')
    ownership_proof = models.FileField(upload_to='hospital-proof-of-ownership', null=True, blank=True)


class HotelOwner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
