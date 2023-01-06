from datetime import datetime
from jdatetime import datetime as jalali_datetime
from decimal import Decimal
import time as moment
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
                          DoctorReviewSerializer, DoctorDateSerializerForAvailableTime,
                          DoctorCreateReviewSerializer, DoctorRetrieveUpdateReviewSerializer)
from django.contrib.gis.geos import Point
from utils.permissions import IsDoctorOrReadOnly, IsWorkDayOwnerOrReadOnly, IsAppointmentOwnerOrReadOnly
from django.db import transaction
from rest_framework.response import Response
from doctorino.pagination import StandardResultsSetPagination
from django.http import HttpResponse, Http404
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
    serializer_class = []
    pagination_class = StandardResultsSetPagination


    def list(self, *args, **kwargs):
        self.serializer_class = DoctorRetrieveUpdateReviewSerializer
        return viewsets.ModelViewSet.list(self, *args, **kwargs)
    
    def retrieve(self, *args, **kwargs):
        self.serializer_class = DoctorRetrieveUpdateReviewSerializer
        return viewsets.ModelViewSet.retrieve(self, *args, **kwargs)

    def create(self, *args, **kwargs):
        self.serializer_class = DoctorCreateReviewSerializer
        return viewsets.ModelViewSet.create(self, *args, **kwargs)

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


class AvailableTimeBaseOnDoctorDate(APIView):

    def count_digits(self, num):
        count = 0
        n = num
        while (n > 0):
            count = count + 1
            n = n // 10
        return count

    def sum_with_hour_quarter(self, time):
        timeList = [str(time), '0:15:00']
        totalSecs = 0
        for tm in timeList:
            timeParts = [int(s) for s in tm.split(':')]
            totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
        totalSecs, sec = divmod(totalSecs, 60)
        hr, min = divmod(totalSecs, 60)
        if self.count_digits(hr) == 1:
            hr = f"0{hr}"
        if self.count_digits(min) == 1:
            min = f"0{min}"
        if self.count_digits(sec) == 1:
            hr = f"0{sec}"
        return f"{hr}:{min}:{sec}"

    def post(self, request, format=None):
        input = DoctorDateSerializerForAvailableTime(data=request.data)
        result = []
        if input.is_valid(raise_exception=True):
            doctor = Doctor.objects.get(id=input.data['doctor'])
            time = jalali_datetime.strptime(input.data['date'], "%Y-%m-%d")
            work_days = WorkDayPeriod.objects.filter(doctor=doctor, day=time.weekday()).order_by("from_time")
            if not work_days.exists():
                return Response({})
            this_time_pointer = work_days[0].from_time
            end_time_date_time = datetime.strptime(f"{input.data['date']} {work_days.last().to_time}", "%Y-%m-%d %H:%M:%S")
            while(True):
                is_available = True
                this_time_end = self.sum_with_hour_quarter(this_time_pointer)
                this_end_date_time = datetime.strptime(f"{input.data['date']} {this_time_end}", "%Y-%m-%d %H:%M:%S")
                if this_end_date_time > end_time_date_time:
                    break
                if not WorkDayPeriod.objects.filter(
                        from_time__lte=this_time_pointer,
                        to_time__gte=this_time_end,
                        day=time.weekday(),
                        doctor=doctor).exists():
                    is_available = False

                if Appointment.objects.filter(
                        to_time__lte=this_time_end,
                        to_time__gt=this_time_pointer,
                        date_reserved=time,
                        doctor=doctor).exists() or \
                        Appointment.objects.filter(
                            from_time__lt=this_time_end,
                            from_time__gte=this_time_pointer,
                            date_reserved=time,
                            doctor=doctor).exists() or \
                        Appointment.objects.filter(
                            from_time__lte=this_time_pointer,
                            to_time__gte=this_time_end,
                            date_reserved=time,
                            doctor=doctor).exists():
                    is_available = False
                result.append({
                    'from_time' : this_time_pointer,
                    'to_time' : this_time_end,
                    'is_available' : is_available
                })
                this_time_pointer = this_time_end
        return Response(result)
'''
{
    "date" : "1400-10-18",
    "doctor" : 2
}
'''