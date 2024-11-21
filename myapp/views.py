from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Patient, Donor
from django.contrib import messages
from django.urls import reverse
from django.db import models  # Import models to use for aggregation
from .models import PatientRequest
from . import forms


# Improved Dashboard View to show blood group count for donors
def donor_dashboard(request):
    if request.user.is_authenticated and hasattr(request.user, 'donor'):
        # Get all donors and count blood groups
        blood_groups = Donor.objects.values('blood_type').annotate(count=models.Count('blood_type'))
        donor_data = {'blood_groups': blood_groups}

        return render(request, 'myapp/donor_dashboard.html', donor_data)
    else:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')

# Admin Dashboard View
def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_staff:
        data = {
            'patients': Patient.objects.all(),
            'donors': Donor.objects.all()
        }
        return render(request, 'myapp/admin_dashboard.html', data)
    else:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')

# Patient Dashboard View
def patient_dashboard(request):
    if request.user.is_authenticated and hasattr(request.user, 'patient'):
        data = {'patient': Patient.objects.get(user=request.user)}
        return render(request, 'myapp/patient_dashboard.html', data)
    else:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')

# Helper function to handle login for different user types
def custom_login(request, user_type, template_name, redirect_view, check_attr):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if hasattr(user, check_attr):  # Check if the user has the specific attribute
                login(request, user)
                messages.success(request, f'{user_type.capitalize()} login successful!')
                return redirect(redirect_view)  # Redirect to specified dashboard
            else:
                messages.error(request, f'User is not a valid {user_type}.')
                return redirect(template_name)  # Redirect back to login page
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect(template_name)  # Redirect back to login page

    return render(request, f'myapp/{template_name}.html')

# Home view
def home(request):
    return render(request, 'myapp/home.html')

# Admin login view
def admin_login(request):
    return custom_login(request, 'admin', 'admin_login', 'admin_dashboard', 'is_staff')

# Patient login view
def patient_login(request):
    return custom_login(request, 'patient', 'patient_login', 'patient_dashboard', 'patient')

# Donor login view
def donor_login(request):
    return custom_login(request, 'donor', 'donor_login', 'donor_dashboard', 'donor')


def donor_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        blood_type = request.POST.get('blood_type')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address', '')  # Address is optional
        age = request.POST.get('age')

        # Validate confirm_password
        if confirm_password is None:
            messages.error(request, 'Confirm password is required.')
            return render(request, 'myapp/donor_register.html')

        # Validate passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'myapp/donor_register.html')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'myapp/donor_register.html')

        # Additional validation for blood type, age, etc.
        if int(age) < 18:
            messages.error(request, 'Age must be 18 or older.')
            return render(request, 'myapp/donor_register.html')

        # Create and save a new User instance
        user = User.objects.create_user(username=username, password=password, email=email)

        # Create and save a new Donor instance
        Donor.objects.create(
            user=user,
            blood_type=blood_type,
            contact_number=contact_number,
            address=address,
            age=age
        )

        # After successful registration, redirect to login page
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('donor_login')

    return render(request, 'myapp/donor_register.html')


def donate_blood(request):
    donation_form=forms.DonationForm()
    if request.method=='POST':
        donation_form=forms.DonationForm(request.POST)
        if donation_form.is_valid():
            blood_donate=donation_form.save(commit=False)
            blood_donate.bloodgroup=donation_form.cleaned_data['bloodgroup']
            donor= models.Donor.objects.get(user_id=request.user.id)
            blood_donate.donor=donor
            blood_donate.save()
            return HttpResponseRedirect('donation_history')  
    return render(request,'myapp/donate_blood.html',{'donation_form':donation_form})

def donation_history(request):
    donor= models.Donor.objects.get(user_id=request.user.id)
    donations=models.BloodDonate.objects.all().filter(donor=donor)
    return render(request,'myapp/donation_history.html',{'donations':donations})




# Patient registration view
def patient_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        blood_type = request.POST.get('blood_type')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address', '')  # Address is optional
        age = request.POST.get('age')

        # Validate confirm_password
        if confirm_password is None:
            messages.error(request, 'Confirm password is required.')
            return render(request, 'myapp/patient_register.html')

        # Validate passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'myapp/patient_register.html')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'myapp/patient_register.html')

        # Additional validation can go here for blood type, age, etc.
        if int(age) < 18:
            messages.error(request, 'Age must be 18 or older.')
            return render(request, 'myapp/patient_register.html')

        # Create and save a new User instance
        user = User.objects.create_user(username=username, password=password, email=email)

        # Create and save a new Patient instance
        Patient.objects.create(
            user=user,
            blood_type=blood_type,
            contact_number=contact_number,
            address=address,
            age=age
        )

        # After successful registration, redirect to login page
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('patient_login')

    return render(request, 'myapp/patient_register.html')

# Logout views
def custom_logout(request, user_type):
    logout(request)
    messages.success(request, f'You have logged out successfully.')
    return redirect('home')

def patient_logout(request):
    return custom_logout(request, 'patient')

def admin_logout(request):
    return custom_logout(request, 'admin')

def donor_logout(request):
    return custom_logout(request, 'donor')
def patient_request_create(request):
    if request.method == 'POST':
        # Handle form submission to create a new patient request
        new_request = PatientRequest.objects.create(
            patient_name=request.POST['patient_name'],
            blood_type=request.POST['blood_type'],
            contact_number=request.POST['contact_number'],
            status=request.POST.get('status', 'pending'),  # Default to 'pending'
        )
        
        # Increment the total requests counter
        total_requests = PatientRequest.objects.count()
        
        # Increment the approved requests counter
        approved_requests = PatientRequest.objects.filter(status='approved').count()
        
        # Pass data back to the template
        messages.success(request, 'Patient request created successfully.')
        return redirect('dashboard')  # Redirect to the dashboard or wherever necessary

    return render(request, 'patient_request_form.html')  # Return the form if not POST
