from django.contrib import admin
from authentication.models import HotelOwner, Doctor,User

admin.site.register(User)
admin.site.register(HotelOwner)
admin.site.register(Doctor)