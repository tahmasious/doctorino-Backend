from django.shortcuts import render
from .models import Doctor, Specialty
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import DoctorSerializer, SpecialtySerializer, DoctorListSerializer
from utils.permissions import IsDoctorOrReadOnly
from django.db import transaction


class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class SpecialtyView(generics.ListAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.filter(is_active=True)
    serializer_class = DoctorListSerializer


class DoctorListCreateViewSet(viewsets.ViewSet):
    queryset = Doctor.objects.all()

    def list(self, request):
        serializer = DoctorListSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = DoctorSerializer(data=request.data)
        print(serializer.initial_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DoctorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = []

    def get_permissions(self): # Retrieve and list don't need authentication, others need
        if self.request.method != "GET":
            return [IsAuthenticated(), IsDoctorOrReadOnly()]
        else:
            return []
        return [permission() for permission in self.permission_classes]


class SpecialityListView(generics.ListAPIView):
    serializer_class = SpecialtySerializer
    queryset = Specialty.objects.all()