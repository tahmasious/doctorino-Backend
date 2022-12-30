from decimal import Decimal
from rest_framework.exceptions import ValidationError
from django.contrib.gis.measure import Distance
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Doctor, Specialty, WorkDayPeriod, Appointment, DoctorReview
from authentication.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import (DoctorDetailSerializer, DoctorListSerializer,
                          DoctorCreateSerializer, SpecialtySerializer, SearchByLocationSpecialtySerializer,
                          WorkDayPeriodSerializer, AppointmentSerializer, DetailedAppointmentSerializer,
                          DoctorReviewSerializer)
from django.contrib.gis.geos import Point
from utils.permissions import IsDoctorOrReadOnly, IsWorkDayOwnerOrReadOnly, IsAppointmentOwnerOrReadOnly
from django.db import transaction
from rest_framework.response import Response
from doctorino.pagination import StandardResultsSetPagination
from django.http import HttpResponse
import json
from django.shortcuts import get_object_or_404

class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.filter(is_active=True)
    pagination_class = StandardResultsSetPagination
    serializer_class = DoctorListSerializer
    authentication_classes = []


class DoctorCreateView(generics.CreateAPIView):
    queryset = Doctor.objects.filter(is_active=True)
    serializer_class = DoctorCreateSerializer
    authentication_classes = []


class DoctorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorDetailSerializer
    permission_classes = []

    def get_permissions(self):  # list doesn't need authentication, others need
        if self.request.method != "GET":
            return [IsAuthenticated(), IsDoctorOrReadOnly()]
        return []


class SpecialtyListView(generics.ListAPIView):
    serializer_class = SpecialtySerializer
    queryset = Specialty.objects.all()
    pagination_class = StandardResultsSetPagination
    authentication_classes = []


def user_id_to_doctor_id(request, **kwargs):
    response_data = {}
    try:
        user = User.objects.get(pk=kwargs['pk'])
        response_data['id'] = user.doctor.pk
    except:
        response_data['id'] = 'None'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


class DoctorSearchByLocationSpecialty(APIView):
    pagination_class = StandardResultsSetPagination
    authentication_classes = []

    def post(self, request, format=None):
        serialized_input = SearchByLocationSpecialtySerializer(data=request.data)
        serialized_input.is_valid(raise_exception=True)
        related_doctors = Doctor.objects.filter(is_active=True)
        if 'lat' in serialized_input.data.keys() and 'long' in serialized_input.data.keys():
            lat = float(serialized_input.data['lat'])
            long = float(serialized_input.data['long'])
            related_doctors = related_doctors.filter(location__distance_lt=(Point(lat, long), Distance(m=5000)))
        if 'specialties' in serialized_input.data.keys():
            specialties = serialized_input.data['specialties']
            related_doctors = related_doctors.filter(specialties__in=specialties)
        if 'province' in serialized_input.data.keys():
            province = serialized_input.data['province']
            related_doctors = related_doctors.filter(province=province)
        serialized_doctors = DoctorListSerializer(related_doctors, many=True)
        return Response(serialized_doctors.data)


class WorkDayPeriodModelViewSet(ModelViewSet):
    serializer_class = WorkDayPeriodSerializer
    queryset = WorkDayPeriod.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        elif self.request.method == "POST":
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated(), IsWorkDayOwnerOrReadOnly()]


class DoctorAllWorkDaysListView(generics.ListAPIView):
    serializer_class = WorkDayPeriodSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if not Doctor.objects.filter(id=self.kwargs['pk']).exists():
            raise ValidationError({
                "error" :  "دکتری با این آیدی به ثبت نرسیده."
            })
        return WorkDayPeriod.objects.filter(doctor_id=self.kwargs['pk'])


class AppointmentModelViewSet(ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        elif self.request.method == "POST":
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated(), IsAppointmentOwnerOrReadOnly()]


class DoctorAllAppointmentsInProfilePageListView(generics.ListAPIView):  # Patients data is not going to be send !
    serializer_class = AppointmentSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if not Doctor.objects.filter(id=self.kwargs['pk']).exists():
            raise ValidationError({
                "error" :  "دکتری با این آیدی به ثبت نرسیده."
            })
        return Appointment.objects.filter(doctor_id=self.kwargs['pk'])


class DetailedDoctorAllAppointmentsListView(generics.ListAPIView):  # include patients data
    serializer_class = DetailedAppointmentSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if not Doctor.objects.filter(id=self.kwargs['pk']).exists():
            raise ValidationError({
                "error" :  "دکتری با این آیدی به ثبت نرسیده."
            })
        return Appointment.objects.filter(doctor_id=self.kwargs['pk'])


class DoctorReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = DoctorReviewSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method != "GET":
            return [IsAuthenticated()]
        return []

    def get_queryset(self):
        if 'pk' not in self.kwargs:
            return DoctorReview.objects.all()

        if not Doctor.objects.filter(id=self.kwargs['pk']).exists():
            raise ValidationError({
                "error": "دکتری با این آیدی به ثبت نرسیده."
            })
        return DoctorReview.objects.filter(doctor_id=self.kwargs['pk'])


class UserDoctorAppoinments(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    pagination_class = StandardResultsSetPagination
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        self.user = get_object_or_404(User, pk=self.kwargs['pk'])
        return Appointment.objects.filter(patient=self.user)
        