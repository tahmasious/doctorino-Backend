from pprint import pprint

from rest_framework import serializers

from authentication.models import HotelOwner, User
from authentication.serializers import UserSerializer, UserListSerializer
from hotel_management.models import Hotel, Room, RoomImage, Feature, HotelReview


class ReadWriteSerializerMethodField(serializers.SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs['source'] = '*'
        super(serializers.SerializerMethodField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return {self.field_name: data}


class HotelOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOwner
        fields = "__all__"


class HotelOwnerCreateSerializer(serializers.ModelSerializer):
    user = ReadWriteSerializerMethodField()

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
        hotel_owner = HotelOwner.objects.create(user=user, **validated_data)
        return hotel_owner


class HotelDetailSerializer(serializers.ModelSerializer):
    hotel_owner = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    rate = serializers.ReadOnlyField()

    class Meta:
        model = Hotel
        fields = "__all__"

    def get_hotel_owner(self, obj):
        hotel_owner = obj.hotel_owner
        return HotelOwnerSerializer(hotel_owner).data

    def get_user(self, obj):
        user = obj.hotel_owner.user
        return UserListSerializer(user).data


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

        if 'features' in validated_data.keys():
            feature_list = validated_data.pop('features')
        hotel = Hotel.objects.create(hotel_owner_id=hotel_owner_id, **validated_data)
        if 'features' in validated_data.keys():
            for feature in feature_list:
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

    class Meta:
        model = RoomImage
        fields = '__all__'

    def create(self, validated_data):
        new_image_room = RoomImage.objects.create(is_cover=validated_data['is_cover'],
                                                  is_thumbnail=validated_data['is_cover'],
                                                  image=validated_data['image'],
                                                  room=validated_data['room'])
        return new_image_room


class RoomSerializer(serializers.ModelSerializer):
    images = ReadWriteSerializerMethodField()

    class Meta:
        model = Room
        fields = ('id', 'hotel', 'quantity', 'bed_count', 'price_per_night', 'images')


    def get_images(self, obj):
        images = RoomImage.objects.filter(room=obj)
        serialized_images = HotelRoomImagesSerializer(images, many=True)
        return serialized_images.data

    def create(self, validated_data):
        if validated_data['hotel']:
            hotel = validated_data['hotel']
        else:
            hotel = self.context['request'].user.hotel
        new_room = Room.objects.create(hotel=hotel,
                                       quantity=validated_data['quantity'],
                                       bed_count=validated_data['bed_count'],
                                       price_per_night=validated_data['price_per_night'])
        new_room.save()

        if "images" in validated_data :
            images = validated_data['images']
            for image in images:
                RoomImage.objects.create(room=new_room,
                                         image=image['image'],
                                         is_thumbnail=image['is_thumbnail'],
                                         is_cover=image['is_cover']).save()

        return new_room


class HotelOwnerUpdateRetrieveSerializer(serializers.ModelSerializer):
    user = ReadWriteSerializerMethodField()

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


class HotelReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelReview
        fields = "__all__"
