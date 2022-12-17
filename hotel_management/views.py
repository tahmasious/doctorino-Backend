from django.db import transaction
from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.views import APIView
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
    HotelReserveSerializer, DetailedHotelReservationSerializer, HotelSearchByLocationSerializer
from utils.permissions import IsHotelOwnerOrReadOnly
from doctorino.pagination import StandardResultsSetPagination
from django.shortcuts import get_object_or_404


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


class HotelAllReservationListView(generics.ListAPIView):
    serializer_class = DetailedHotelReservationSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if not Hotel.objects.filter(id=self.kwargs['pk']).exists():
            raise ValidationError({
                "error" :  "هتلی با این آیدی به ثبت نرسیده."
            })
        return HotelReservation.objects.filter(hotel_id=self.kwargs['pk'])


class HotelSearchByLocation(APIView):
    permission_classes = []
    authentication_classes = []
    pagination_class = StandardResultsSetPagination

    def post(self, request, format=None):
        query = HotelSearchByLocationSerializer(data=request.data)
        query.is_valid(raise_exception=True)
        related_hotels = Hotel.objects.all()
        if 'lat' in query.data.keys() and 'long' in query.data.keys():
            lat = float(query.data['lat'])
            long = float(query.data['long'])
            related_hotels = related_hotels.filter(location__distance_lt=(Point(lat, long), Distance(m=5000)))

        serialized_hotels = HotelListSerializer(related_hotels, many=True)
        return Response(serialized_hotels.data)


class HotelAvailableRooms(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    pagination_class = StandardResultsSetPagination
    serializer_class = RoomSerializer
    
    def get_queryset(self):
        result = []
        print("-------------------------")
        self.hotel = get_object_or_404(Hotel, pk=self.kwargs['pk'])
        print(self.hotel)

        self.from_date = self.kwargs['from']
        print(self.from_date)
        self.to_date = self.kwargs['to']
        rooms_of_hotel = Room.objects.filter(hotel=self.hotel)

        for room in rooms_of_hotel:
            reserves_of_room = HotelReservation.objects.filter(hotel_room=room)
            case_1 = reserves_of_room.filter(to_date__gt=self.from_date, to_date__lte=self.to_date).count()     
            
            # --------start_requested-----(----end_requested----)
            case_2 = reserves_of_room.filter(from_date__lt=self.to_date, from_date__gte=self.from_date).count()

            # ----(---start_requested----------end_requested----)
            case_3 = reserves_of_room.filter(from_date__lt=self.from_date, to_date__gt=self.to_date).count()
            
            # ---------start_requested(--------)end_requested-----
            case_4 = reserves_of_room.filter(from_date__gte= self.from_date, to_date__lte=self.to_date).count()

            number_of_reserved = case_1 + case_2 + case_3 - case_4
            if number_of_reserved < room.quantity:
                result.append(room)

        return result
