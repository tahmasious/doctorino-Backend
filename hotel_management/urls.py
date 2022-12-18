from django.urls import path, include, register_converter
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from .views import HotelRetrieveUpdateDestroyView, RoomRetrieveUpdateDestroyView, RoomListCreateView, \
    HotelRoomsListView, HotelRoomImageCreateView, HotelCreateView, FeatureListView, HotelListView, HotelOwnerUpdateView,\
    HotelOwnerCreateView, HotelReviewListCreateView, HotelImageCreateView, \
    HotelImageDestroyView, \
    HotelOwnerHotelsListView, HotelReservationModelViewSet, HotelAllReservationListView, \
    HotelSearchByLocation, HotelAvailableRooms

from .converters import DateConverter

register_converter(DateConverter, 'date')

app_name = 'hotel_management'
hotel_reserve_router = DefaultRouter()
hotel_reserve_router.register(r'', HotelReservationModelViewSet, basename="hotel_reserve")

urlpatterns = [
    # Hotel urls
    path('<int:pk>/', HotelRetrieveUpdateDestroyView.as_view()),
    path('', HotelListView.as_view()),
    path('new/', HotelCreateView.as_view()),
    path('<int:pk>/room/', HotelRoomsListView.as_view()),
    path('image/', HotelImageCreateView.as_view()),
    path('image/<int:pk>/', HotelImageDestroyView.as_view()),

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

    # hotel reserve endpoints
    path('hotel_reserve/', include(hotel_reserve_router.urls)),
    path('<int:pk>/hotel_reserve/', HotelAllReservationListView.as_view()),
    path('<int:pk>/<date:from>/<date:to>/available_rooms/', HotelAvailableRooms.as_view()),

    # search endpoint
    path('search/', HotelSearchByLocation.as_view()),

    # hotel reviews
    path('reviews/', HotelReviewListCreateView.as_view()),
    path('<int:pk>/reviews/', HotelReviewListCreateView.as_view())
]

