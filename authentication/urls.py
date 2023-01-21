from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from authentication.views import UserCreationView, CustomTokenObtainPairView, \
    PatientCreateView, PatientRetrieveUpdateDestroyView, SendVerificationCode, VerifyVerificationCode, SetNewPassword, \
    BaseUserNameUpdate

from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view()),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view()),
    path('new-user/', UserCreationView.as_view()),
    path('patient/<int:pk>/', PatientRetrieveUpdateDestroyView.as_view()),
    path('patient/new/', PatientCreateView.as_view()),
    path('change-password/send-code/', SendVerificationCode.as_view()),
    path('change-password/verify/', VerifyVerificationCode.as_view()),
    path('change-password/set-password/', SetNewPassword.as_view()),
    path('base-user/name/', BaseUserNameUpdate.as_view())
]