from django.urls import path, include
from rest_framework import routers

from .views import HotelRetrieveUpdateDestroyView, RoomRetrieveUpdateDestroyView, RoomListCreateView, \
    HotelRoomsListView, HotelRoomImageCreateView, HotelListCreateViewSet, FeatureListView

router = routers.DefaultRouter()
router.register(r'', HotelListCreateViewSet)

urlpatterns = [
    # Hotel urls
    path('<int:pk>/', HotelRetrieveUpdateDestroyView.as_view()),
    path('', include(router.urls)),
    path('<int:pk>/room/', HotelRoomsListView.as_view()),

    # Room urls
    path('room/', RoomListCreateView.as_view()),
    path('room/<int:pk>/', RoomRetrieveUpdateDestroyView.as_view()),
    path('room/image/', HotelRoomImageCreateView.as_view()),

    # Features urls
    path('feature/', FeatureListView.as_view())
]

