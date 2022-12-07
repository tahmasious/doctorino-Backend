from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from authentication.views import UserCreationView
from rest_framework import routers
from .views import (DoctorListView, DoctorCreateView,
                    DoctorRetrieveUpdateDestroyView, SpecialtyListView,
                    user_id_to_doctor_id, DoctorSearchByLocationSpecialty, WorkDayPeriodModelViewSet,
                    AppointmentModelViewSet, DoctorAllWorkDaysListView, DoctorAllAppointmentsInProfilePageListView,
                    DetailedDoctorAllAppointmentsListView)


app_name = 'doctor_management'
workday_router = DefaultRouter()
workday_router.register(r'', WorkDayPeriodModelViewSet, basename="workday")

appointment_router = DefaultRouter()
appointment_router.register(r'', AppointmentModelViewSet, basename='appointment')

urlpatterns = [
    path('<int:pk>/', DoctorRetrieveUpdateDestroyView.as_view()),
    path('', DoctorListView.as_view()),
    path('new/', DoctorCreateView.as_view()),
    
    path('specialties/', SpecialtyListView.as_view()),

    path('user_id_to_doctor_id/<int:pk>/', user_id_to_doctor_id),

    # search endpoint
    path('search/', DoctorSearchByLocationSpecialty.as_view()),

    # work day period times endpoint
    path('workday/', include(workday_router.urls)),
    path('<int:pk>/workday/', DoctorAllWorkDaysListView.as_view()),  # all workdays of a specific doctor

    # appointment endpoints
    path('appointment/', include(appointment_router.urls)),  # new - delete - update - retrieve - list
    path('<int:pk>/appointment/', DoctorAllAppointmentsInProfilePageListView.as_view()),  # all appointments of specific doctor for profile page
    path('<int:pk>/appointment/detailed/', DetailedDoctorAllAppointmentsListView.as_view())  #  all appointments of specific doctor for doctor panel
]