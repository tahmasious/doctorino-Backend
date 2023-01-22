import json

from rest_framework import serializers
from rest_framework.response import Response
import time
from .models import Doctor, Specialty, WorkDayPeriod, Appointment, DoctorReview
from authentication.models import User
from authentication.serializers import UserSerializer, UserListSerializer, UserCommonInfoSerializer, \
    UserSimpleInfoSerializer
from django_jalali.serializers.serializerfield import JDateField, JDateTimeField


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
    specialties = ReadWriteSerializerMethodField()
    work_periods = serializers.SerializerMethodField()
    rate = serializers.ReadOnlyField()
    city = ReadWriteSerializerMethodField()
    province = ReadWriteSerializerMethodField()

    class Meta:
        model = Doctor
        fields = "__all__"

    def get_user(self, obj):
        user = obj.user
        return UserListSerializer(user).data

    def get_specialties(self, obj):
        specialties = obj.specialties.all()
        return SpecialtySerializer(specialties, many=True).data

    def get_work_periods(self, obj):
        work_periods = WorkDayPeriod.objects.filter(doctor=obj)
        return WorkDayPeriodSerializer(work_periods, many=True).data

    def get_city(self, obj):
        return obj.get_city_display()

    def get_province(self, obj):
        return obj.get_province_display()


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
        user.is_doctor = True
        user.save()

        doctor = Doctor.objects.create(user=user, **validated_data)
        for spec in specialty_list:
            doctor.specialties.add(spec)
        doctor.save()
        return doctor


class DoctorListSerializer(serializers.ModelSerializer):
    specialties = serializers.SerializerMethodField()
    user = UserCommonInfoSerializer()
    rate = serializers.ReadOnlyField()
    city = serializers.SerializerMethodField()
    province = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        exclude = ('license_proof', 'is_active', 'national_code',)

    def get_specialties(self, obj):
        specialties = obj.specialties.all()
        serializer = SpecialtySerializer(specialties, many=True)
        return serializer.data

    def get_city(self, obj):
        return obj.get_city_display()

    def get_province(self, obj):
        return obj.get_province_display()

class SearchByLocationSpecialtySerializer(serializers.Serializer):
    lat = serializers.DecimalField(required=False, max_digits=9, decimal_places=6)
    long = serializers.DecimalField(required=False, max_digits=9, decimal_places=6)
    specialties = serializers.ListSerializer(required=False, child=serializers.IntegerField(allow_null=False))
    province = serializers.IntegerField(required=False)

class WorkDayPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkDayPeriod
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    date_reserved = JDateField()

    class Meta:
        model = Appointment
        fields = "__all__"

    def validate(self, attrs):
        errs = dict()
        data = super(AppointmentSerializer, self).validate(attrs)
        if Appointment.objects.filter(                        # -------(-----2(pm)------)-------4(pm)------------
                to_time__lte=data['to_time'],
                to_time__gt=data['from_time'],
                date_reserved=data['date_reserved'],
                doctor=data['doctor']).exists() or \
        Appointment.objects.filter(                           # --------------2(pm)------(-------4(pm)--------)----
                from_time__lt=data['to_time'],
                from_time__gte=data['from_time'],
                date_reserved=data['date_reserved'],
                doctor=data['doctor']).exists() or \
        Appointment.objects.filter(                           # ------(--------2(pm)--------------4(pm)--------)----
                from_time__lte=data['from_time'],
                to_time__gte=data['to_time'],
                date_reserved=data['date_reserved'],
                doctor=data['doctor']).exists():
            errs['from_time'] = ['این تایم رزرو با تایم ها اکتیو قبلی تداخل دارد']
            errs['to_time'] = ['این تایم رزرو با تایم ها اکتیو قبلی تداخل دارد']
        if data['to_time'] < data['from_time'] :
            errs['from_time'] = ["زمان شروع دوره نباید بعد از زمان پایان دوره کاری باشد."]
        if errs:
            raise serializers.ValidationError(errs)
        return data


class DetailedAppointmentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    date_reserved = JDateField()

    class Meta:
        model = Appointment
        fields = "__all__"

    def get_user(self, obj):
        return UserListSerializer(obj.patient).data


class DoctorCreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorReview
        fields = "__all__"


class DoctorDateSerializerForAvailableTime(serializers.Serializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.filter(is_active=True))
    date = JDateField()


class DoctorRetrieveUpdateReviewSerializer(serializers.ModelSerializer):
    voter = serializers.SerializerMethodField()

    class Meta:
        model = DoctorReview
        fields = "__all__"

    def get_voter(self, obj):
        return UserSimpleInfoSerializer(obj.voter).data


class DoctorUpdateSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = "__all__"

    def get_user(self, obj):
        return UserListSerializer(obj.user).data

    # def update(self, instance: Doctor, validated_data):
    #     validated_data = dict(validated_data)
    #     if 'user' in validated_data:
    #         user_data = validated_data.pop('user')
    #         user = instance.user
    #         if type(user_data) != dict:
    #             user_data = json.loads(user_data)
    #         user_serialized = UserSerializer(data=user)
    #         user_serialized.is_valid()
    #         user_serialized.update(user, user_data)
    #         User.objects.filter(id=instance.user.id).update(**user_data)
    #     return super(DoctorUpdateSerializer, self).update(instance, validated_data)
