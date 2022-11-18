from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from .views import Hotel, HotelRetrieveUpdateDestroyView, RoomRetrieveUpdateDestroyView, RoomListCreateView, \
    HotelListCreateView, HotelRoomsListView, HotelRoomImageCreateView
from authentication.views import UserCreationView



urlpatterns = [
    # Hotel urls
    path('<int:pk>/', HotelRetrieveUpdateDestroyView.as_view()),
    path('', HotelListCreateView.as_view()),
    path('<int:pk>/room/', HotelRoomsListView.as_view()),

    # Room urls
    path('room/', RoomListCreateView.as_view()),
    path('room/<int:pk>/', RoomRetrieveUpdateDestroyView.as_view()),
    path('room/image/', HotelRoomImageCreateView.as_view())
]

