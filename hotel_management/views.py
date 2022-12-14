from django.db import transaction
from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.models import HotelOwner
from doctorino.pagination import StandardResultsSetPagination
from hotel_management.models import Hotel, Room, RoomImage, Feature, HotelReservation
from hotel_management.serializer import HotelCreateSerializer, RoomSerializer, HotelRoomImagesSerializer, \
    HotelListSerializer, \
    FeatureSerializer, HotelDetailSerializer, HotelOwnerUpdateRetrieveSerializer, HotelOwnerCreateSerializer,\
    HotelReserveSerializer
from utils.permissions import IsHotelOwnerOrReadOnly
from doctorino.pagination import StandardResultsSetPagination


class HotelRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelDetailSerializer
    permission_classes = []

    def get_permissions(self): # Retrieve and list don't need authentication, others need
        if self.request.method != "GET":
            return [IsAuthenticated(), IsHotelOwnerOrReadOnly()]
        else:
            return []
        return [permission() for permission in self.permission_classes]


class HotelListView(generics.ListAPIView):
    queryset = Hotel.objects.filter(is_active=True)
    pagination_class = StandardResultsSetPagination
    serializer_class = HotelListSerializer


class HotelCreateView(generics.CreateAPIView):
    queryset = Hotel.objects.filter(is_active=True)
    serializer_class = HotelCreateSerializer
    permission_classes = [IsAuthenticated,]


class RoomRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = []

    def get_permissions(self): # Retrieve and list don't need authentication, others need
        if self.request.method != "GET":
            return [IsAuthenticated(), IsHotelOwnerOrReadOnly()]
        else:
            return []
        return [permission() for permission in self.permission_classes]

class RoomListCreateView(generics.ListCreateAPIView):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    pagination_class = StandardResultsSetPagination


class HotelRoomsListView(generics.ListAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        return Room.objects.filter(hotel_id=self.kwargs["pk"])


class HotelRoomImageCreateView(generics.CreateAPIView):
    serializer_class = HotelRoomImagesSerializer
    queryset = RoomImage.objects.all()


class FeatureListView(generics.ListAPIView):
    serializer_class = FeatureSerializer
    queryset = Feature.objects.all()
    pagination_class = StandardResultsSetPagination


class HotelOwnerUpdateView(generics.RetrieveUpdateAPIView):
    queryset = HotelOwner.objects.all()
    serializer_class = HotelOwnerUpdateRetrieveSerializer


class HotelOwnerCreateView(generics.CreateAPIView):
    queryset = HotelOwner.objects.all()
    serializer_class = HotelOwnerCreateSerializer
    permission_classes = []


class HotelOwnerHotelsListView(generics.ListAPIView):
    serializer_class = HotelListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if not (self.request.user.is_hotel_owner or self.request.user.is_superuser) :
            context = {'user' : ['شما دسترسی برای دیدن هتل ها ندارید !']}
            raise ValidationError(detail=context)
        hotel_owner_id = self.request.user.owner.filter().last().id
        return Hotel.objects.filter(hotel_owner_id=hotel_owner_id)


class HotelReservationModelViewSet(ModelViewSet):
    serializer_class = HotelReserveSerializer
    queryset = HotelReservation.objects.all()
    pagination_class = StandardResultsSetPagination
