from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from authentication.views import UserCreationView
from rest_framework import routers
from .views import (DoctorListView, DoctorCreateView,
                    DoctorRetrieveUpdateDestroyView, SpecialtyListView,
                    user_id_to_doctor_id, DoctorSearchByLocationSpecialty)


app_name = 'doctor_management'


urlpatterns = [
    path('<int:pk>/', DoctorRetrieveUpdateDestroyView.as_view()),
    path('', DoctorListView.as_view()),
    path('new/', DoctorCreateView.as_view()),
    
    path('specialties/', SpecialtyListView.as_view()),

    path('user_id_to_doctor_id/<int:pk>/', user_id_to_doctor_id),

    # search
    path('search/', DoctorSearchByLocationSpecialty.as_view())
]