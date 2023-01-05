import datetime

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from authentication.models import HotelOwner, User
from doctorino.pagination import StandardResultsSetPagination
from hotel_management.models import Hotel, Room, RoomImage, Feature, HotelReservation
from hotel_management.models import HotelReview, HotelImage
from hotel_management.serializer import HotelCreateSerializer, RoomSerializer, HotelRoomImagesSerializer, \
    HotelListSerializer, \
    HotelReviewSerializer, HotelImageSerializer, \
    FeatureSerializer, HotelDetailSerializer, HotelOwnerUpdateRetrieveSerializer, HotelOwnerCreateSerializer, \
    HotelReserveSerializer, DetailedHotelReservationSerializer, HotelSearchByLocationSerializer
from utils.permissions import IsHotelOwnerOrReadOnly, HasHotelOwnerRole, IsRoomOwnerOrReadOnly, IsOwnerOrReadOnly, \
    IsHotelReserveOwnerOrReadOnly


class HotelRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelDetailSerializer
    permission_classes = []

    def get_permissions(self):  # list doesn't need authentication, others need
        if self.request.method != "GET":
            return [IsAuthenticated(), IsHotelOwnerOrReadOnly()]
        return []


class HotelListView(generics.ListAPIView):
    queryset = Hotel.objects.filter(is_active=True)
    pagination_class = StandardResultsSetPagination
    serializer_class = HotelListSerializer


class HotelCreateView(generics.CreateAPIView):
    queryset = Hotel.objects.filter(is_active=True)
    serializer_class = HotelCreateSerializer
    # permission_classes = [IsAuthenticated, HasHotelOwnerRole]


class RoomRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = []

    def get_permissions(self):
        if self.request.method != "GET":
            return [IsAuthenticated(), IsRoomOwnerOrReadOnly()]
        return []

class RoomListCreateView(generics.ListCreateAPIView):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):  # list doesn't need authentication, others need
        if self.request.method != "GET":
            return [IsAuthenticated()]
        return []

class HotelRoomsListView(generics.ListAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        return Room.objects.filter(hotel_id=self.kwargs["pk"])


class HotelRoomImageCreateView(generics.CreateAPIView):
    serializer_class = HotelRoomImagesSerializer
    queryset = RoomImage.objects.all()
    permission_classes = [HasHotelOwnerRole]

class FeatureListView(generics.ListAPIView):
    serializer_class = FeatureSerializer
    queryset = Feature.objects.all()
    pagination_class = StandardResultsSetPagination


class HotelOwnerUpdateView(generics.RetrieveUpdateAPIView):
    queryset = HotelOwner.objects.all()
    serializer_class = HotelOwnerUpdateRetrieveSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

class HotelOwnerCreateView(generics.CreateAPIView):
    queryset = HotelOwner.objects.all()
    serializer_class = HotelOwnerCreateSerializer


class HotelOwnerHotelsListView(generics.ListAPIView):
    serializer_class = HotelListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if not (self.request.user.is_hotel_owner or self.request.user.is_superuser) :
            context = {'user' : ['شما دسترسی برای دیدن هتل ها ندارید !']}
            raise ValidationError(detail=context)
        hotel_owner_id = self.request.user.owner.id
        return Hotel.objects.filter(hotel_owner_id=hotel_owner_id)


class HotelReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = HotelReviewSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method != "GET":
            return [IsAuthenticated()]
        return []

    def get_queryset(self):
        if 'pk' not in self.kwargs:
            return HotelReview.objects.all()

        if not Hotel.objects.filter(id=self.kwargs['pk']).exists():
            raise ValidationError({
                "error": "دکتری با این آیدی به ثبت نرسیده."
            })
        return HotelReview.objects.filter(hotel_id=self.kwargs['pk'])


class HotelImageCreateView(generics.CreateAPIView):
    serializer_class = HotelImageSerializer
    queryset = HotelImage.objects.all()
    permission_classes = [IsAuthenticated, HasHotelOwnerRole]


class HotelImageDestroyView(generics.DestroyAPIView):
    serializer_class = HotelImageSerializer
    queryset = HotelImage.objects.all()
    permission_classes = [IsAuthenticated, HasHotelOwnerRole]


class HotelReservationModelViewSet(ModelViewSet):
    serializer_class = HotelReserveSerializer
    queryset = HotelReservation.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        elif self.request.method == "POST":
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated(), IsHotelReserveOwnerOrReadOnly()]


class HotelAllReservationListView(generics.ListAPIView):
    serializer_class = DetailedHotelReservationSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if not Hotel.objects.filter(id=self.kwargs['pk']).exists():
            raise ValidationError({
                "error" :  "هتلی با این آیدی به ثبت نرسیده."
            })
        
        return HotelReservation.objects.filter(hotel_room__hotel_id=self.kwargs['pk'])


class HotelSearchByLocation(APIView):
    pagination_class = StandardResultsSetPagination

    def post(self, request, format=None):
        query = HotelSearchByLocationSerializer(data=request.data)
        query.is_valid(raise_exception=True)
        related_hotels = Hotel.objects.all()

        if 'lat' in query.data.keys() and 'long' in query.data.keys():
            lat = float(query.data['lat'])
            long = float(query.data['long'])
            related_hotels = related_hotels.filter(location__distance_lt=(Point(lat, long), Distance(m=5000)))

        if 'province' in query.data.keys():
            province = query.data['province']
            related_hotels = related_hotels.filter(province=province)
        
        serialized_hotels = HotelListSerializer(related_hotels, many=True)
        return Response(serialized_hotels.data)


class HotelAvailableRooms(generics.ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = RoomSerializer

    def get_queryset(self):
        result = []
        self.hotel = get_object_or_404(Hotel, pk=self.kwargs['pk'])
        self.from_date = self.kwargs['from']
        self.to_date = self.kwargs['to']

        errs = {}

        if self.from_date < datetime.date.today():
            errs['before today'] = ['نمیتوان برای قبل از امروز رزرو کرد.']
            raise ValidationError(errs)

        if self.from_date > self.to_date:
            errs['start after end'] = ['تاریخ اتمام رزرو نمیتواند قبل از تاریخ شروع آن باشد.']
            raise ValidationError(errs)

        if self.from_date == self.to_date:
            errs['start equal to end'] = ['تاریخ شروع روزر و پایان آن نباید برابر باشد']
            raise ValidationError(errs)
    
        rooms_of_hotel = Room.objects.filter(hotel=self.hotel)

        for room in rooms_of_hotel:
            reserves_of_room = HotelReservation.objects.filter(hotel_room=room)

            # ----(---start_requested---)------end_requested-----
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


class UserHotelReservations(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    pagination_class = StandardResultsSetPagination
    serializer_class = HotelReserveSerializer

    def get_queryset(self):
        result = []
        self.user = get_object_or_404(User, pk=self.kwargs['pk'])
        return HotelReservation.objects.filter(customer=self.user)
        