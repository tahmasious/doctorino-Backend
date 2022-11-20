from django.db import models
from authentication.models import User
# Create your models here.

class Specialty(models.Model):
    name = models.CharField(max_length=250, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female'),
        (2, 'not specified'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    ownership_proof = models.FileField(upload_to='doctor-proof-of-being-doctor', null=True, blank=True)
    medical_system_number = models.CharField(max_length=8, unique=True, blank=False, null=True)
    is_verifyed = models.BooleanField(default=False, blank=True, null=True)
    natinal_code = models.CharField(max_length=10, unique=True, blank=False, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=2)
    specialties = models.ManyToManyField(Specialty)
    clinic_address = models.CharField(max_length=250, blank=True, null=False)

    def __str__(self):
        return self.user.username