from rest_framework import serializers
from .models import Doctor, Specialty
from authentication.serializers import UserSerializer, UserListSerializer
from authentication.models import User


class ReadWriteSerializerMethodField(serializers.SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs['source'] = '*'
        super(serializers.SerializerMethodField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return {self.field_name: data}


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = '__all__'


class DoctorDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = "__all__"

    def get_user(self, obj):
        user = obj.user
        return UserListSerializer(user).data


class DoctorCreateSerializer(serializers.ModelSerializer):
    user = ReadWriteSerializerMethodField()

    class Meta:
        model = Doctor
        fields = (
            "id", 
            "user", 
            "medical_system_number", 
            "gender",
            "specialties", 
            "province", 
            "city", 
            "clinic_address"
        )


    def get_user(self, obj):
        user = obj.user
        return UserListSerializer(user).data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        specialty_list = validated_data.pop('specialties')

        user_serialized = UserSerializer(data=user_data)
        user_serialized.is_valid(raise_exception=True)
        user = user_serialized.save()
        
        doctor = Doctor.objects.create(user=user, **validated_data)
        for spec in specialty_list:
            doctor.specialties.add(spec)
        doctor.save()
        return doctor


class DoctorListSerializer(serializers.ModelSerializer):
    specialties = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        exclude = ('license_proof', 'is_active', 'national_code',)

    def get_specialties(self, obj):
        specialties = obj.specialties.all()
        serializer = SpecialtySerializer(specialties, many=True)
        return serializer.data