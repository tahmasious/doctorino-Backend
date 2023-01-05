from django.urls import path, include, register_converter
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from .views import HotelRetrieveUpdateDestroyView, RoomRetrieveUpdateDestroyView, RoomListCreateView, \
    HotelRoomsListView, HotelRoomImageCreateView, HotelCreateView, FeatureListView, HotelListView, HotelOwnerUpdateView,\
    HotelOwnerCreateView, HotelReviewListCreateView, HotelImageCreateView, \
    HotelImageDestroyView, \
    HotelOwnerHotelsListView, HotelReservationModelViewSet, HotelAllReservationListView, \
    HotelSearchByLocation, HotelAvailableRooms, UserHotelReservations, \
    SuggestHotelAcordingToDoctorLocationView

from .converters import DateConverter

register_converter(DateConverter, 'date')

app_name = 'hotel_management'
hotel_reserve_router = DefaultRouter()
hotel_reserve_router.register(r'', HotelReservationModelViewSet, basename="hotel_reserve")

urlpatterns = [
    # Hotel urls                                                  # permissions
    path('<int:pk>/', HotelRetrieveUpdateDestroyView.as_view()),  # retrieve : all, update and destroy : only obj owner
    path('', HotelListView.as_view()),                            # all
    path('new/', HotelCreateView.as_view()),                      # only hotel owner
    path('<int:pk>/room/', HotelRoomsListView.as_view()),         # all
    path('image/', HotelImageCreateView.as_view()),               # the hotel obj owner
    path('image/<int:pk>/', HotelImageDestroyView.as_view()),     # the hotel obj owner

    # Room urls
    path('room/', RoomListCreateView.as_view()),                  # list :all , create : only hotel owner
    path('room/<int:pk>/', RoomRetrieveUpdateDestroyView.as_view()),  # room retrieve : all , others : owner obj
    path('room/image/', HotelRoomImageCreateView.as_view()),      # only hotel room obj owner

    # Features urls
    path('feature/', FeatureListView.as_view()),                  # all

    # owner urls
    path('owner/<int:pk>/', HotelOwnerUpdateView.as_view()),      #hotel owner obj
    path('owner/new/', HotelOwnerCreateView.as_view()),           #all
    path('owner/hotel-list/', HotelOwnerHotelsListView.as_view()),#all

    # hotel reserve endpoints
    path('hotel_reserve/', include(hotel_reserve_router.urls)),                              # all
    path('<int:pk>/hotel_reserve/', HotelAllReservationListView.as_view()),                  # all
    path('<int:pk>/<date:from>/<date:to>/available_rooms/', HotelAvailableRooms.as_view()),  # all
    # search endpoint
    path('search/', HotelSearchByLocation.as_view()),             # all

    # hotel reviews
    path('reviews/', HotelReviewListCreateView.as_view()),        # list : all , create : logged in user only
    path('<int:pk>/reviews/', HotelReviewListCreateView.as_view()),# list : all , create : logged in user only

    path('<int:pk>/user_reservations/', UserHotelReservations.as_view()),

    path('suggest_hotel/', SuggestHotelAcordingToDoctorLocationView.as_view()),
]
