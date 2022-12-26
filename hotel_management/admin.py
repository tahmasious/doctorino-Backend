from django.contrib import admin
from hotel_management.models import Hotel, Room, RoomImage, Feature, HotelReview, HotelImage

from hotel_management.models import Hotel, Room, RoomImage, Feature, HotelReservation

class HotelAdmin(admin.ModelAdmin):
    list_display = ("hotel_owner", "trade_code", "hotel_name", "hotel_stars", "is_active", "city")
    list_filter = ("hotel_owner", "hotel_name")

    class Meta:
        model = Hotel

admin.site.register(Hotel, HotelAdmin)


class HotelRoomAdmin(admin.ModelAdmin):
    list_display = ("hotel", "quantity", "bed_count")
admin.site.register(Room, HotelRoomAdmin)

admin.site.register(RoomImage)
admin.site.register(Feature)
admin.site.register(HotelReservation)

admin.site.register(HotelReview)
admin.site.register(HotelImage)