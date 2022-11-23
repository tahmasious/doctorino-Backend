from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from authentication.views import UserCreationView
from rest_framework import routers
from .views import (DoctorListView, DoctorCreateView,
                    DoctorRetrieveUpdateDestroyView, SpecialtyListView)


app_name = 'doctor_management'


urlpatterns = [
    path('<int:pk>/', DoctorRetrieveUpdateDestroyView.as_view()),
    path('', DoctorListView.as_view()),
    path('new/', DoctorCreateView.as_view()),
    
    path('specialties/', SpecialtyListView.as_view())
]