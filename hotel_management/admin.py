from django.contrib import admin
from hotel_management.models import Hotel, Room, RoomImage, Feature, HotelReview, HotelImage


class HotelAdmin(admin.ModelAdmin):
    list_display = ("hotel_owner", "trade_code", "hotel_name", "hotel_stars", "is_active")
    list_filter = ("hotel_owner", "hotel_name")

    class Meta:
        model = Hotel

admin.site.register(Hotel, HotelAdmin)


admin.site.register(Room)
admin.site.register(RoomImage)
admin.site.register(Feature)
admin.site.register(HotelReview)
admin.site.register(HotelImage)