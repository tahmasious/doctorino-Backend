
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from hotel_management.models import Hotel
from hotel_management.serializer import HotelSerializer
from utils.permissions import IsHotelOwnerOrReadOnly


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = []

    def get_permissions(self): # Retrieve and list don't need authentication, others need
        if self.request.method != "GET":
            return [IsAuthenticated(), IsHotelOwnerOrReadOnly()]
        else:
            return []
        return [permission() for permission in self.permission_classes]