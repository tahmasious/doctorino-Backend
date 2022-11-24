from django.db import transaction
from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.models import HotelOwner
from doctorino.pagination import StandardResultsSetPagination
from hotel_management.models import Hotel, Room, RoomImage, Feature
from hotel_management.serializer import HotelCreateSerializer, RoomSerializer, HotelRoomImagesSerializer, \
    HotelListSerializer, \
    FeatureSerializer, HotelDetailSerializer, HotelOwnerSerializer, HotelOwnerUpdateRetrieveSerializer
from utils.permissions import IsHotelOwnerOrReadOnly


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
    authentication_classes = []


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


class HotelOwnerUpdateView(generics.RetrieveUpdateAPIView):
    queryset = HotelOwner.objects.all()
    serializer_class = HotelOwnerUpdateRetrieveSerializer

