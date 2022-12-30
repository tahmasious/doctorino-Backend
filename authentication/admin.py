from django.contrib import admin
from authentication.models import User, HotelOwner, Patient

admin.site.register(User)
admin.site.register(HotelOwner)

@admin.action(description='update doctor city and province')
def update_patient_city(modeladmin, request, queryset):
    queryset.update(city=0,province=0)

class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'code_melli', 'phone_number','city','province')
    actions = [update_patient_city]
admin.site.register(Patient, PatientAdmin)
