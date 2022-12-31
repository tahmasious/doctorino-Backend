from django.urls import path, include, register_converter
from hotel_management.views import SuggestHotelAcordingToDoctorLocView


urlpatterns = [
    path('suggest_hotel/<int:appointment_pk>/', SuggestHotelAcordingToDoctorLocView.as_view()),
]