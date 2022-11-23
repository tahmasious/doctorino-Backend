from django.shortcuts import render
from .models import Doctor, Specialty
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import (DoctorDetailSerializer, DoctorListSerializer,
                        DoctorCreateSerializer, SpecialtySerializer)

from utils.permissions import IsDoctorOrReadOnly
from django.db import transaction
from rest_framework.response import Response
from doctorino.pagination import StandardResultsSetPagination


class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.filter(is_active=True)
    pagination_class = StandardResultsSetPagination
    serializer_class = DoctorListSerializer


class DoctorCreateView(generics.CreateAPIView):
    queryset = Doctor.objects.filter(is_active=True)
    serializer_class = DoctorCreateSerializer


class DoctorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorDetailSerializer
    permission_classes = []

    def get_permissions(self): # Retrieve and list don't need authentication, others need
        if self.request.method != "GET":
            return [IsAuthenticated(), IsDoctorOrReadOnly()]
        else:
            return []
        return [permission() for permission in self.permission_classes]


class SpecialtyListView(generics.ListAPIView):
    serializer_class = SpecialtySerializer
    queryset = Specialty.objects.all()