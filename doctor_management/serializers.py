from rest_framework import serializers
from .models import Doctor, Specialty
from authentication.serializers import UserSerializer


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


class DoctorSerializer(serializers.ModelSerializer):
    user = ReadWriteSerializerMethodField()
    specialties = SpecialtySerializer()

    class Meta:
        model = Doctor
        fields = '__all__'

    def get_user(self, obj):
        user = obj.user
        return UserSerializer(user).data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        user.set_password(user_data['password'])
        doctor = Doctor.objects.create(user=user, **validated_data)
        doctor.save()
        return doctor


class DoctorListSerializer(serializers.ModelSerializer):
    specialties = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        exclude = ('license_proof', 'is_verifyed', 'natinal_code',)

    def get_specialties(self, obj):
        specialties = obj.specialties.all()
        serializer = FeatureSerializer(specialties, many=True)
        return serializer.data