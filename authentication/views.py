from rest_framework import generics
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.models import User, HotelOwner, Patient
from hotel_management.models import Hotel
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, UserListSerializer, \
    UserProfileSerializer, PatientCreateSerializer, PatientDetailSerializer, \
    PatientUpdateSerializer

from utils.permissions import IsPatientOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class UserCreationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer


class PatientCreateView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientCreateSerializer
    authentication_classes = []


class PatientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientDetailSerializer
    permission_classes = []

    def get_permissions(self):  # retrieve doesn't need authentication, others need
        if self.request.method != "GET":
            return [IsAuthenticated(), IsPatientOwnerOrReadOnly()]
        return []

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PatientDetailSerializer
        if self.request.method == 'PUT':
            return PatientUpdateSerializer
        return DoctorDetailSerializer
