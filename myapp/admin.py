from django.contrib import admin
from .models import Patient, Donor

class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_type', 'contact_number', 'address', 'age', 'date_of_birth', 'gender')
    search_fields = ('user__first_name', 'user__last_name', 'blood_type', 'contact_number')  # Search by first name, last name, etc.
    list_filter = ('blood_type', 'gender')  # Filter by blood type and gender

class DonorAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_type', 'contact_number', 'address', 'age', 'donation_date')
    search_fields = ('user__first_name', 'user__last_name', 'blood_type', 'contact_number')  # Search by first name, last name, etc.
    list_filter = ('blood_type',)  # Filter by blood type

# Register models with custom admins
admin.site.register(Patient, PatientAdmin)
admin.site.register(Donor, DonorAdmin)
