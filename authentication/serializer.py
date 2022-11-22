from pprint import pprint

from rest_framework import serializers
from .models import User, Doctor
from hotel_management.models import Hotel


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        new_user = User.objects.create(username=validated_data['username'])
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user
