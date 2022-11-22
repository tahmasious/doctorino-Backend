from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from .views import DoctorViewSet
from authentication.views import UserCreationView
from rest_framework import routers
from .views import DoctorRetrieveUpdateDestroyView, SpecialityListView

app_name = 'doctor_management'

router = routers.SimpleRouter()
router.register('', DoctorViewSet)


urlpatterns = [
    path('<int:pk>/', DoctorRetrieveUpdateDestroyView.as_view()),
    path('', include(router.urls)),
    path('specialities/', SpecialityListView.as_view()),
]