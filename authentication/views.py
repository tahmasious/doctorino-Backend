from rest_framework import generics
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.models import User, HotelOwner
from hotel_management.models import Hotel
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, UserListSerializer, \
    UserProfileSerializer

from rest_framework.viewsets import ModelViewSet


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = []

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        # if self.action == 'retrieve':
        #     return UserProfileSerializer
        return UserSerializer

# class UserCreationView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     authentication_classes = []


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer
