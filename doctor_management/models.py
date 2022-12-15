from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from authentication.models import User
from django.contrib.gis.db import models as lcmodels
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django_jalali.db import models as jmodels
from rest_framework import serializers

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
    license_proof = models.FileField(upload_to='doctor-proof-of-being-doctor', null=True, blank=True)
    medical_system_number = models.CharField(max_length=8, unique=True, blank=False, null=True)
    is_active = models.BooleanField(default=False, blank=True, null=True)
    national_code = models.CharField(max_length=10, unique=True, blank=False, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=2)
    specialties = models.ManyToManyField(Specialty)
    province = models.CharField(max_length=50, blank=False, null=True)
    city = models.CharField(max_length=50, blank=False, null=True)
    clinic_address = models.CharField(max_length=250, blank=True, null=True)
    image = models.ImageField(upload_to='doctor-image', blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=False, null=True)
    office_number = models.CharField(max_length=11, blank=False, null=True)
    education = models.CharField(max_length=50, blank=False, null=True)
    location = lcmodels.PointField(geography=True, default=Point(0.0, 0.0))
    description = models.TextField(max_length=7000, null=True, blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def rate(self):
        query = DoctorReview.objects.filter(doctor=self)
        if not query.exists():
            return 0
        count = len(query)
        sum = 0
        for review in query:
            sum += review.score
        return round(float(sum/count), 2)


class WorkDayPeriod(models.Model):
    WEEK_DAY_CHOICES = (
        (0, "شنبه"),
        (1, "یک شنبه"),
        (2, "دو شنبه"),
        (3, "سه شنبه"),
        (4, "چهارشنبه"),
        (5, "پنج شنبه"),
        (6, "جمعه"),
    )

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=WEEK_DAY_CHOICES)
    from_time = models.TimeField()
    to_time = models.TimeField()

    def clean(self, *args, **kwargs):
        if self.from_time and self.to_time:
            if self.from_time > self.to_time :
                raise ValidationError(
                    {"from_time": "زمان شروع دوره نباید بعد از زمان پایان دوره کاری باشد."}
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_reserved = jmodels.jDateField()
    from_time = models.TimeField()
    to_time = models.TimeField()
    patient_name = models.CharField(max_length=256, blank=False, null=True)
    national_code = models.CharField(max_length=10, blank=False, null=True)

    def clean(self):
        errs = dict()
        if self.from_time and self.to_time :
            if self.from_time > self.to_time:
                errs['from_time'] = ["زمان شروع دوره نباید بعد از زمان پایان دوره کاری باشد."]
        if errs:
            raise ValidationError(errs)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class DoctorReview(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField(null=True, blank=True)