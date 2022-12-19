from pprint import pprint

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "id", "email")


class UserCommonInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({'username': self.user.username})
        data.update({'id': self.user.id})
        data.update({'is_hotel_owner': self.user.is_hotel_owner})
        data.update({'is_doctor': self.user.is_doctor})
        if self.user.is_doctor:
            child_id = self.user.doctor.id
        elif self.user.is_hotel_owner:
            child_id = self.user.owner.id
        else:
            child_id = self.user.id
        data.update({'child-id' : child_id})
        data.update({'first-name' : self.user.first_name})
        data.update({'last-name' : self.user.last_name})
        # and everything else you want to send in the response
        return data