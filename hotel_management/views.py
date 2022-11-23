from django.db import transaction
from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hotel_management.models import Hotel, Room, RoomImage, Feature
from hotel_management.serializer import HotelSerializer, RoomSerializer, HotelRoomImagesSerializer, HotelListSerializer, \
    FeatureSerializer
from utils.permissions import IsHotelOwnerOrReadOnly


class HotelRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = []

    def get_permissions(self): # Retrieve and list don't need authentication, others need
        if self.request.method != "GET":
            return [IsAuthenticated(), IsHotelOwnerOrReadOnly()]
        else:
            return []
        return [permission() for permission in self.permission_classes]


class HotelListCreateViewSet(viewsets.ViewSet):
    queryset = Hotel.objects.all()

    def list(self, request):
        serializer = HotelListSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = HotelSerializer(data=request.data)
        print(serializer.initial_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoomRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()


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
