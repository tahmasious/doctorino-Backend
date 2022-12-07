from rest_framework import serializers
from rest_framework.response import Response

from .models import Doctor, Specialty, WorkDayPeriod, Appointment
from authentication.serializers import UserSerializer, UserListSerializer, UserCommonInfoSerializer
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
    specialties = serializers.SerializerMethodField()
    work_periods = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = "__all__"

    def get_user(self, obj):
        user = obj.user
        return UserListSerializer(user).data

    def get_specialties(self, obj):
        specialties = obj.specialties
        return SpecialtySerializer(specialties, many=True).data

    def get_work_periods(self, obj):
        work_periods = WorkDayPeriod.objects.filter(doctor=obj)
        return WorkDayPeriodSerializer(work_periods, many=True).data


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
    user = UserCommonInfoSerializer()
    
    class Meta:
        model = Doctor
        exclude = ('license_proof', 'is_active', 'national_code',)

    def get_specialties(self, obj):
        specialties = obj.specialties.all()
        serializer = SpecialtySerializer(specialties, many=True)
        return serializer.data


class SearchByLocationSpecialtySerializer(serializers.Serializer):
    lat = serializers.DecimalField(required=False, max_digits=9, decimal_places=6)
    long = serializers.DecimalField(required=False, max_digits=9, decimal_places=6)
    specialties = serializers.ListSerializer(required=False, child=serializers.IntegerField(allow_null=False))


class WorkDayPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkDayPeriod
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"


class DetailedAppointmentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = "__all__"

    def get_user(self, obj):
        return UserListSerializer(obj.user).data
