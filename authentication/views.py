from rest_framework import generics
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.models import User, HotelOwner
from hotel_management.models import Hotel
from .serializers import UserSerializer, CustomTokenObtainPairSerializer


class UserCreationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer
