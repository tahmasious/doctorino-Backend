from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from authentication.views import UserCreationView, CustomTokenObtainPairView

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view()),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view()),
    path('new-user/', UserCreationView.as_view()),
]