from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=120, unique=True, blank=False, null=True)
    is_hotel_owner = models.BooleanField(default=False, blank=True, null=True)
    is_doctor = models.BooleanField(default=False, blank=True, null=True)
    email = models.EmailField(unique=True, blank=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hospital_owner')
    ownership_proof = models.FileField(upload_to='hospital-proof-of-ownership', null=True, blank=True)


class HotelOwner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    shaba_code = models.CharField(max_length=256, null=True, blank=True)