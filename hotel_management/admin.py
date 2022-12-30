from django.contrib import admin
from hotel_management.models import Hotel, Room, RoomImage, Feature, HotelReview, HotelImage

from hotel_management.models import Hotel, Room, RoomImage, Feature, HotelReservation

@admin.action(description='update doctor city and province')
def update_hotel_city(modeladmin, request, queryset):
    queryset.update(city=0,province=0)

class HotelAdmin(admin.ModelAdmin):
    #list_display = ("hotel_owner", "trade_code", "hotel_name", "hotel_stars", "is_active", "city")
    list_filter = ("hotel_owner", "hotel_name")
    actions = [update_hotel_city]

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