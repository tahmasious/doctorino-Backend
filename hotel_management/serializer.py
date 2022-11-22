from rest_framework import serializers
from hotel_management.models import Hotel, Room, RoomImage, Feature


class ReadWriteSerializerMethodField(serializers.SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs['source'] = '*'
        super(serializers.SerializerMethodField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return {self.field_name: data}


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = "__all__"


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"


class HotelListSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        exclude = ('ownership_proof', 'hotel_description', 'rules', 'hotel_owner')

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
        print(validated_data)
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