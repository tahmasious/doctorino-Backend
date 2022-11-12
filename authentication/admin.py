from django.contrib import admin
from authentication.models import Doctor, User

admin.site.register(User)
admin.site.register(Doctor)