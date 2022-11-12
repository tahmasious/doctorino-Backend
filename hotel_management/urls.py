from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from .views import Hotel, HotelViewSet
from authentication.views import UserCreationView
app_name = 'hotel_management'
router = DefaultRouter()
router.register(r'', HotelViewSet, basename="")
urlpatterns = router.urls
