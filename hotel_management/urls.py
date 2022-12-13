from django.urls import path, include
from rest_framework import routers

from .views import HotelRetrieveUpdateDestroyView, RoomRetrieveUpdateDestroyView, RoomListCreateView, \
    HotelRoomsListView, HotelRoomImageCreateView, HotelCreateView, FeatureListView, HotelListView, HotelOwnerUpdateView, \
    HotelOwnerCreateView, HotelOwnerHotelsListView, HotelReviewListCreateView

urlpatterns = [
    # Hotel urls
    path('<int:pk>/', HotelRetrieveUpdateDestroyView.as_view()),
    path('', HotelListView.as_view()),
    path('new/', HotelCreateView.as_view()),
    path('<int:pk>/room/', HotelRoomsListView.as_view()),

    # Room urls
    path('room/', RoomListCreateView.as_view()),
    path('room/<int:pk>/', RoomRetrieveUpdateDestroyView.as_view()),
    path('room/image/', HotelRoomImageCreateView.as_view()),

    # Features urls
    path('feature/', FeatureListView.as_view()),

    # owner urls
    path('owner/<int:pk>/', HotelOwnerUpdateView.as_view()),          # update and retrieve
    path('owner/new/', HotelOwnerCreateView.as_view()),               # create new hotel owner
    path('owner/hotel-list/', HotelOwnerHotelsListView.as_view()),

    # hotel reviews
    path('reviews/', HotelReviewListCreateView.as_view()),
    path('<int:pk>/reviews/', HotelReviewListCreateView.as_view())
]

