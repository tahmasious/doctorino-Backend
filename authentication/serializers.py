from pprint import pprint

from rest_framework import serializers
from .models import User
from doctor_management.models import Doctor


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        print(validated_data)
        new_user = User.objects.create(username=validated_data['username'])
        new_user.set_password(validated_data['password'])
        new_user.save()
        if 'is_doctor' in validated_data.keys() and validated_data['is_doctor']:
            new_user.is_doctor = True
            new_user.save()
            new_doctor = Doctor.objects.create(user=new_user)
            new_doctor.save()
        elif 'is_hotel_owner' in validated_data.keys() and validated_data['is_hotel_owner']:
            new_user.is_hotel_owner = True
            new_user.save()
            new_hotel_owner = HotelOwner.objects.create(user=new_user)
            new_hotel_owner.save()
        return new_user