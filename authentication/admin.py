from django.contrib import admin
from authentication.models import User, HotelOwner, Patient

admin.site.register(User)
admin.site.register(HotelOwner)
admin.site.register(Patient)
