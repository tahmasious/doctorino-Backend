from pprint import pprint

from rest_framework import serializers
from django_jalali.serializers.serializerfield import JDateField, JDateTimeField
from authentication.models import HotelOwner, User
from authentication.serializers import UserSerializer, UserListSerializer
from hotel_management.models import Hotel, Room, RoomImage, Feature, HotelReview, HotelImage
from hotel_management.models import Hotel, Room, RoomImage, Feature, HotelReservation
import datetime


class ReadWriteSerializerMethodField(serializers.SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs['source'] = '*'
        super(serializers.SerializerMethodField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return {self.field_name: data}


class HotelOwnerSerializer(serializers.ModelSerializer):
    birth_day = JDateField()

    class Meta:
        model = HotelOwner
        fields = "__all__"


class HotelOwnerCreateSerializer(serializers.ModelSerializer):
    user = ReadWriteSerializerMethodField()
    birth_day = JDateField()

    class Meta:
        model = HotelOwner
        fields = "__all__"

    def get_user(self, obj):
        user = obj.user
        return UserSerializer(user).data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serialized = UserSerializer(data=user_data)
        user_serialized.is_valid(raise_exception=True)
        user = user_serialized.save()
        user.is_hotel_owner = True
        user.save()

        hotel_owner = HotelOwner.objects.create(user=user, **validated_data)
        return hotel_owner


class HotelDetailSerializer(serializers.ModelSerializer):
    hotel_owner = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    rate = serializers.ReadOnlyField()
    features = ReadWriteSerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = "__all__"

    def get_hotel_owner(self, obj):
        hotel_owner = obj.hotel_owner
        return HotelOwnerSerializer(hotel_owner).data

    def get_user(self, obj):
        user = obj.hotel_owner.user
        return UserListSerializer(user).data

    def get_features(self, obj):
        features = obj.features.all()
        serializer = FeatureSerializer(features, many=True)
        return serializer.data

    def get_images(self, obj):
        images = HotelImage.objects.filter(hotel_id=obj.id)
        return  HotelImageSerializer(images, many=True).data

class HotelCreateSerializer(serializers.ModelSerializer):
    hotel_owner = ReadWriteSerializerMethodField(required=False)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ("id", "hotel_owner", "cover_image", "user", "hotel_name", "hotel_stars", "address", "features")

    def get_hotel_owner(self, obj):
        hotel_owner = obj.hotel_owner
        return HotelOwnerSerializer(hotel_owner).data

    def get_user(self, obj):
        user = obj.hotel_owner.user
        return UserListSerializer(user).data

    def validate(self, attrs):
        errs = dict()
        data = super().validate(attrs)
        if 'hotel_owner' in data:
            if not HotelOwner.objects.filter(id=data['hotel_owner']).exists():
                errs['hotel_owner'] = ["هیچ صاحب هتلی با این pk یافت نشد!"]
        else:
            if not self.context['request'].user.is_hotel_owner and not self.context['request'].user.is_superuser:
                errs['hotel_owner'] = ['شما دسترسی ساخت هتل ندارید !']
            else:
                user_id = self.context['request'].user.id
                if not HotelOwner.objects.filter(user_id=user_id).exists():
                    errs['hotel_owner'] = ['حساب خام شما ساخته شده اما حساب مدیریت هتل شما ساخته نشده است !']
        if errs:
            raise serializers.ValidationError(errs)
        return data

    def create(self, validated_data):
        if 'hotel_owner' in validated_data :
            hotel_owner_id = validated_data['hotel_owner']
        else:
            user_id = self.context['request'].user.id
            hotel_owner_id = HotelOwner.objects.filter(user_id=user_id).last().id
        feature_list = None
        if 'features' in validated_data.keys():
            feature_list = validated_data.pop('features')
            print(feature_list)
        hotel = Hotel.objects.create(hotel_owner_id=hotel_owner_id, **validated_data)
        if feature_list:
            for feature in feature_list:
                print(feature)
                hotel.features.add(feature)
        hotel.save()
        return hotel


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"


class HotelListSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()
    rate = serializers.ReadOnlyField()

    class Meta:
        model = Hotel
        exclude = ('trade_code', 'hotel_description', 'rules', 'hotel_owner')

    def get_features(self, obj):
        features = obj.features.all()
        serializer = FeatureSerializer(features, many=True)
        return serializer.data


class HotelRoomImagesSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        errs = dict()
        data = super(HotelRoomImagesSerializer, self).validate(attrs)
        if self.context['request'].method == "POST":
            if data['room'].hotel.hotel_owner.user != self.context['request'].user:
                errs['room'] = ['شما فقط به اتاق های خود می توانید عکس اضافه کنید !']
        if errs:
            raise serializers.ValidationError(errs)
        return data
    class Meta:
        model = RoomImage
        fields = '__all__'

    def create(self, validated_data):
        new_image_room = RoomImage.objects.create(**validated_data)
        return new_image_room


class RoomSerializer(serializers.ModelSerializer):
    images = ReadWriteSerializerMethodField()

    def validate(self, attrs):
        errs = dict()
        data = super(RoomSerializer, self).validate(attrs)
        if self.context['request'].method == 'POST':
            if data['hotel'].hotel_owner != self.context['request'].user.owner:
                errs['hotel'] = ['شما فقط برای هتل خود می توانید اتاق اضافه کنید !']
        if errs:
            raise serializers.ValidationError(errs)
        return data
    class Meta:
        model = Room
        fields = ('id', 'hotel', 'quantity', 'bed_count', 'price_per_night', 'images', 'room_title')


    def get_images(self, obj):
        images = RoomImage.objects.filter(room=obj)
        serialized_images = HotelRoomImagesSerializer(images, many=True)
        return serialized_images.data

    def create(self, validated_data):
        if "images" in validated_data:
            images = validated_data.pop('images')
        new_room = Room.objects.create(**validated_data)
        new_room.save()

        if "images" in validated_data :
            for image in images:
                RoomImage.objects.create(room=new_room,
                                         image=image['image'],
                                         is_thumbnail=image['is_thumbnail'],
                                         is_cover=image['is_cover']).save()

        return new_room


class HotelOwnerUpdateRetrieveSerializer(serializers.ModelSerializer):
    user = ReadWriteSerializerMethodField()
    birth_day = JDateField()

    class Meta:
        model = HotelOwner
        fields = "__all__"

    def get_user(self, obj):
        return UserListSerializer(obj.user).data

    def update(self, instance: HotelOwner, validated_data):
        if 'user' in validated_data:
            user_data = validated_data.pop('user')
            user = instance.user
            UserSerializer().update(user, user_data)
            User.objects.filter(id=instance.user.id).update(**user_data)
        return super(HotelOwnerUpdateRetrieveSerializer, self).update(instance, validated_data)


class HotelReserveSerializer(serializers.ModelSerializer):
    from_date = JDateField()
    to_date = JDateField()

    class Meta:
        model = HotelReservation
        fields = "__all__"

    def validate(self, attrs):
        errs = dict()
        data = super(HotelReserveSerializer, self).validate(attrs)

        if data['from_date'] < datetime.date.today():
            errs['before today'] = ['نمیتوان برای قبل از امروز رزرو کرد.']
            raise serializers.ValidationError(errs)

        if data['from_date'] > data['to_date']:
            errs['start after end'] = ['تاریخ اتمام رزرو نمیتواند قبل از تاریخ شروع آن باشد.']
            raise serializers.ValidationError(errs)

        if data['from_date'] == data['to_date']:
            errs['start equal to end'] = ['تاریخ شروع روزر و پایان آن نباید برابر باشد']
            raise serializers.ValidationError(errs)

        room = Room.objects.get(pk=data['hotel_room'].id)

        reserves_of_room = HotelReservation.objects.filter(hotel_room=room)

        # ----(---start_requested----)-----end_requested----
        case_1 = reserves_of_room.filter(to_date__gt=data['from_date'], to_date__lte=data['to_date']).count()

        # --------start_requested-----(----end_requested----)
        case_2 = reserves_of_room.filter(from_date__lt=data['to_date'], from_date__gte=data['from_date']).count()

        # ----(---start_requested----------end_requested----)
        case_3 = reserves_of_room.filter(from_date__lt=data['from_date'], to_date__gt=data['to_date']).count()

        #---------start_requested(--------)end_requested-----
        case_4 = reserves_of_room.filter(from_date__gte= data['from_date'], to_date__lte=data['to_date']).count()

        number_of_reserved = case_1 + case_2 + case_3 - case_4

        if number_of_reserved >= room.quantity:
            errs['room_full'] = ['ظرفیت این اتاق پر است.']

        if errs:
            raise serializers.ValidationError(errs)
        return data


class DetailedHotelReservationSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()

    class Meta:
        model = HotelReservation
        fields = "__all__"

    def get_customer(self, obj):
        return UserListSerializer(obj.customer).data


class HotelSearchByLocationSerializer(serializers.Serializer):
    lat = serializers.DecimalField(required=False, max_digits=9, decimal_places=6)
    long = serializers.DecimalField(required=False, max_digits=9, decimal_places=6)
    city = serializers.IntegerField(required=False)

class HotelReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelReview
        fields = "__all__"


class HotelImageSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        errs =dict()
        data = super(HotelImageSerializer, self).validate(attrs)
        if data['hotel'].hotel_owner != self.context['request'].user.owner:
            errs['error'] = ['شما فقط برای هتل خودتان می توانید عکس انتخاب کنید !']
        if errs:
            raise serializers.ValidationError(errs)
        return data

    class Meta:
        model = HotelImage
        fields = "__all__"
