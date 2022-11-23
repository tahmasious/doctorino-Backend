from django.contrib import admin
from authentication.models import User, HotelOwner

admin.site.register(User)
admin.site.register(HotelOwner)