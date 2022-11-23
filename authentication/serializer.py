from pprint import pprint

from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        new_user = User.objects.create(email=validated_data['email'])
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "id", "email")
