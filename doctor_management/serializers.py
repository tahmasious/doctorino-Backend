from rest_framework import serializers
from .models import Doctor, Specialty


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
