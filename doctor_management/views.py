from decimal import Decimal

from django.contrib.gis.measure import Distance
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Doctor, Specialty, WorkDayPeriod
from authentication.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import (DoctorDetailSerializer, DoctorListSerializer,
                          DoctorCreateSerializer, SpecialtySerializer, SearchByLocationSpecialtySerializer,
                          WorkDayPeriodSerializer)
from django.contrib.gis.geos import Point
from utils.permissions import IsDoctorOrReadOnly
from django.db import transaction
from rest_framework.response import Response
from doctorino.pagination import StandardResultsSetPagination
from django.http import HttpResponse
import json

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


def user_id_to_doctor_id(request, **kwargs):
    response_data = {}
    try:
        user = User.objects.get(pk=kwargs['pk'])
        response_data['id'] = user.doctor.pk
    except:
        response_data['id'] = 'None'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


class DoctorSearchByLocationSpecialty(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, format=None):
        query_date = SearchByLocationSpecialtySerializer(data=request.data)
        query_date.is_valid(raise_exception=True)
        related_doctors = Doctor.objects.all()
        if 'lat' in query_date.data.keys() and 'long' in query_date.data.keys():
            lat = float(query_date.data['lat'])
            long = float(query_date.data['long'])
            related_doctors = related_doctors.filter(location__distance_lt=(Point(lat, long), Distance(m=5000)))
        if 'specialties' in query_date.data.keys():
            specialties = query_date.data['specialties']
            related_doctors = related_doctors.filter(specialties__in=specialties)
        serialized_doctors = DoctorListSerializer(related_doctors, many=True)
        return Response(serialized_doctors.data)


class WorkDayPeriodModelViewSet(ModelViewSet):
    serializer_class = WorkDayPeriodSerializer
    queryset = WorkDayPeriod.objects.all()
