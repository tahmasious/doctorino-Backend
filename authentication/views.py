from rest_framework import generics
from rest_framework import viewsets
from authentication.models import User
from hotel_management.models import Hotel
from authentication.serializer import UserSerializer


class UserCreationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []


