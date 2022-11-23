from django.contrib import admin
from authentication.models import Doctor, User, HotelOwner

admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(HotelOwner)