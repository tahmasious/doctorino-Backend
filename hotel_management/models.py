from django.db import models
from authentication.models import User


class Hotel(models.Model):
    hotel_owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hotel')
    ownership_proof = models.FileField(upload_to='hotel-proof-of-ownership', null=True, blank=True)
    hotel_name = models.CharField(max_length=256, null=True)
    hotel_stars = models.SmallIntegerField(null=True)
    hotel_description = models.CharField(max_length=1024, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    rules = models.CharField(max_length=256, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.hotel_name