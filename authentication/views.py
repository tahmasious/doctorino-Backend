import datetime
import random
from django.conf import settings
from django.core.mail import send_mail

from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from authentication.models import User, HotelOwner, Patient, VerificationCode
from doctor_management.serializers import DoctorDetailSerializer
from doctorino.pagination import StandardResultsSetPagination
from hotel_management.models import Hotel
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, UserListSerializer, \
    UserProfileSerializer, PatientCreateSerializer, PatientDetailSerializer, \
    PatientUpdateSerializer

from utils.permissions import IsPatientOwnerOrReadOnly, IsObjectOwnerOrReadOnly
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


def get_random_string(length):
    final = ''
    letters = '1234567890'
    for i in range(length):
        final = f"{final}{letters[random.randint(0,len(letters) -1)]}"
    return final


class SendVerificationCode(APIView):
    def post(self, request, format=None):
        if 'email' in request.data :
            user = User.objects.filter(email=request.data.get('email'))
            if user.exists():
                user = user.first()
                code = get_random_string(4)
                # send code
                subject = 'درخواست تغییر رمز حساب دکترینو'
                message = f'کد تایید شما برای درخواست تغییر رمز :{code} '
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email, ]
                try:
                    send_mail(subject, message, email_from, recipient_list)
                except Exception as e:
                    print(e)
                    return Response({'error' : 'خطا در ارسال ایمیل'}, status=status.HTTP_400_BAD_REQUEST)

                # end email
                code_obj = VerificationCode.objects.create(code=code, user=user)
                code_obj.save()
                return Response({'status' : 'ok'}, status=status.HTTP_200_OK)
            return Response({'error' : 'هیچ کاربری با این ایمیل ثبت نشده'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error' : 'bad parameters'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyVerificationCode(APIView):
    def post(self, request, format=None):
        if 'email' in request.data and 'code' in request.data:
            user = User.objects.filter(email=request.data.get('email'))
            if user.exists():
                if len(request.data.get('code')) != 4:
                    return Response({'error': 'کد تایید باید چهار رقمی باشد'}, status=status.HTTP_400_BAD_REQUEST)
                user = user.first()
                now_time = datetime.datetime.now()
                code_objs = VerificationCode.objects.filter(
                    code=request.data.get('code'),
                    user=user, is_used=False,
                    creation_datetime__gte=now_time - datetime.timedelta(hours=0, minutes=2)).order_by('-creation_datetime')
                if not code_objs.exists():
                    return Response({'error': 'کد نامعتبر است'}, status=status.HTTP_400_BAD_REQUEST)
                if code_objs.first().code != int(request.data.get('code')):
                    return Response({'error': 'کد نامعتبر است'}, status=status.HTTP_400_BAD_REQUEST)
                code_objs.update(is_used=True)
                return Response({'status' : 'ok'}, status=status.HTTP_200_OK)
            return Response({'error' : 'هیچ کاربری با این ایمیل ثبت نشده'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error' : 'bad parameters'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPassword(APIView):
    def post(self, request, format=None):
        if 'email' in request.data and 'password' in request.data:
            user = User.objects.filter(email=request.data.get('email'))
            if user.exists():
                user = user.first()
                now_time = datetime.datetime.now()
                code_objs = VerificationCode.objects.filter(
                    user=user, is_used=True,
                    creation_datetime__gte=now_time - datetime.timedelta(hours=0, minutes=20)).order_by(
                    '-creation_datetime')
                if not code_objs.exists():
                    return Response({'error': 'حساب خود را دوباره تایید کنید'}, status=status.HTTP_400_BAD_REQUEST)
                user.set_password(request.data.get('password'))
                user.save()
                return Response({'status': 'ok'}, status=status.HTTP_200_OK)
            return Response({'error': 'هیچ کاربری با این ایمیل ثبت نشده'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'bad parameters'}, status=status.HTTP_400_BAD_REQUEST)


class BaseUserNameUpdate(APIView):
    permission_classes = [IsObjectOwnerOrReadOnly, IsAuthenticated]
    def put(self, request, format=None):
        if 'id' in request.data:
            user = User.objects.filter(id=request.data.get('id'))
            if user.exists():
                user = user.first()
                if 'first-name' in request.data:
                    first_name = request.data.get('first-name')
                    user.first_name = first_name
                if 'last-name' in request.data:
                    last_name = request.data.get('last-name')
                    user.last_name = last_name
                user.save()
                return Response({'status': 'ok'}, status=status.HTTP_200_OK)
            return Response({'error': 'هیچ کاربری با این آیدی ثبت نشده'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'bad parameters'}, status=status.HTTP_400_BAD_REQUEST)
