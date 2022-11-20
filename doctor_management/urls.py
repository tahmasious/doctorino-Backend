from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from .views import DoctorViewSet
from authentication.views import UserCreationView
from rest_framework import routers

app_name = 'doctor_management'

router = routers.SimpleRouter()
router.register('', DoctorViewSet)
urlpatterns = router.urls
