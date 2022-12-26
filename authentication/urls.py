from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from authentication.views import UserModelViewSet, CustomTokenObtainPairView

from rest_framework.routers import DefaultRouter

user_router = DefaultRouter()
user_router.register(r'', UserModelViewSet, basename='user')


urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view()),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view()),
    # path('new-user/', UserCreationView.as_view()),
    path('new-user/', include(user_router.urls)),

]