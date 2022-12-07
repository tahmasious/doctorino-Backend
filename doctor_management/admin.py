from django.contrib import admin
from .models import Doctor, Specialty, WorkDayPeriod, Appointment

admin.site.register(Doctor)
admin.site.register(Specialty)
admin.site.register(WorkDayPeriod)
admin.site.register(Appointment)