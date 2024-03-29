from pprint import pprint

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django_jalali.serializers.serializerfield import JDateField, JDateTimeField
from .models import User, Patient, HotelOwner


class ReadWriteSerializerMethodField(serializers.SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs['source'] = '*'
        super(serializers.SerializerMethodField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return {self.field_name: data}


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
            try:
                child_id = self.user.patient.id
            except:
                child_id = self.user.id
                
        data.update({'child-id' : child_id})
        data.update({'first-name' : self.user.first_name})
        data.update({'last-name' : self.user.last_name})
        data.update({'email' : self.user.email})
        # and everything else you want to send in the response
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "birth_day")


class PatientCreateSerializer(serializers.ModelSerializer):
    user = ReadWriteSerializerMethodField()
    birth_day = JDateField(required=False)
    city = ReadWriteSerializerMethodField(required=False)
    province = ReadWriteSerializerMethodField(required=False)

    class Meta:
        model = Patient
        fields = '__all__'


    def get_user(self, obj):
        user = obj.user
        return UserListSerializer(user).data

    def get_city(self, obj):
        return obj.get_city_display()

    def get_province(self, obj):
        return obj.get_province_display()

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        user_serialized = UserSerializer(data=user_data)
        user_serialized.is_valid(raise_exception=True)
        user = user_serialized.save()
        user.save()

        patient = Patient.objects.create(user=user, **validated_data)
        patient.save()
        return patient


class PatientDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    birth_day = JDateField()
    city = ReadWriteSerializerMethodField()
    province = ReadWriteSerializerMethodField()

    class Meta:
        model = Patient
        fields = "__all__"

    def get_user(self, obj):
        user = obj.user
        return UserListSerializer(user).data

    def get_city(self, obj):
        return obj.get_city_display()

    def get_province(self, obj):
        return obj.get_province_display()


class PatientUpdateSerializer(serializers.ModelSerializer):
    user = ReadWriteSerializerMethodField()

    class Meta:
        model = Patient
        fields = "__all__"

    def get_user(self, obj):
        return UserListSerializer(obj.user).data

    def update(self, instance: Patient, validated_data):
        if 'user' in validated_data:
            user_data = validated_data.pop('user')
            user = instance.user
            UserSerializer().update(user, user_data)
            User.objects.filter(id=instance.user.id).update(**user_data)
        return super(PatientUpdateSerializer, self).update(instance, validated_data)


class UserSimpleInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name")