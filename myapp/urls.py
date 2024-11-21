from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('patient_login/', views.patient_login, name='patient_login'),
    path('donor_login/', views.donor_login, name='donor_login'),
    path('donor_register/', views.donor_register, name='donor_register'),
    path('donor_dashboard', views.donor_dashboard,name='donor_dashboard'),
    
    path('donate_blood/', views.donate_blood,name='donate_blood'),
    path('donation_history/', views.donation_history,name='donation_history'),
    
    path('patient_register/', views.patient_register, name='patient_register'),
    path('patient_logout/', views.patient_logout, name='patient_logout'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),  # Add this line for admin logout
    path('donor_logout/', views.donor_logout, name='donor_logout'),  # Add this line for donor logout
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),  # Patient dashboard
    path('patient-request/', views.patient_request_create, name='patient_request_create'),
]
