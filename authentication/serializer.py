from pprint import pprint

from rest_framework import serializers
from .models import User, Doctor, HotelOwner


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        print(validated_data)
        new_user = User.objects.create(username=validated_data['username'])
        new_user.set_password(validated_data['password'])
        new_user.save()
        if validated_data['is_hotel_owner']:
            new_doctor = Doctor.objects.create(user=new_user)
            new_doctor.save()
        elif validated_data['is_doctor']:
            new_hotel_owner = HotelOwner.objects.create(user=new_user)
            new_hotel_owner.save()
        return new_user
