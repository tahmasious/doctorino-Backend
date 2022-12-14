from django.contrib import admin
from hotel_management.models import Hotel, Room, RoomImage, Feature, HotelReservation

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(RoomImage)
admin.site.register(Feature)
admin.site.register(HotelReservation)
