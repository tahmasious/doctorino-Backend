from django.contrib import admin
from .models import Doctor, Specialty, WorkDayPeriod, Appointment, DoctorReview


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'national_code', 'is_active', 'gender', 'city')
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Specialty)

class WorkDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'day', 'from_time', 'to_time')
admin.site.register(WorkDayPeriod, WorkDayAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'date_reserved', 'from_time', 'to_time')
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(DoctorReview)
