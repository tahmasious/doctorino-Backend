from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=120, unique=True, blank=False, null=True)
    is_hotel_owner = models.BooleanField(default=False, blank=True, null=True)
    is_doctor = models.BooleanField(default=False, blank=True, null=True)
