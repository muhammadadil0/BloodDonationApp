from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Home Page
    path('', views.home, name='home'),
    
    # Admin URLs
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),

    # Donor URLs
    path('donor_login/', views.donor_login, name='donor_login'),
    path('donor_register/', views.donor_register, name='donor_register'),
    path('donor_dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('donate_blood/', views.donate_blood, name='donate_blood'),
    path('donation_history/', views.donation_history, name='donation_history'),
    path('donor_logout/', views.donor_logout, name='donor_logout'),

    # Patient URLs
    path('patient_login/', views.patient_login, name='patient_login'),
    path('patient_register/', views.patient_register, name='patient_register'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient_logout/', views.patient_logout, name='patient_logout'),
    path('patient-request/', views.patient_request_create, name='patient_request_create'),
    path('my_request/', views.my_request, name='my_request'),
    path('makerequest/', views.make_request, name='makerequest'),
    # Additional URLs
    path('contact-us/', views.contact_us, name='contact_us'),
    path('all_donor_history/', views.all_donor_history, name='all_donor_history'),
    path('all_patient_history/', views.all_patient_history, name='all_patient_history'),
    path('blood_stock/', views.blood_stock_view, name='blood_stock'),

    # Default Logout (For non-specific users)
    path('logout/', LogoutView.as_view(), name='logout'),
]
