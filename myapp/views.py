import json
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import BloodRequest, Patient, Donor, BloodDonate
from django.contrib import messages
from django.urls import reverse
from django.db import models  # Import models to use for aggregation
from .models import PatientRequest
from . import forms

from .forms import BloodRequestForm, ContactUsForm 

from django.shortcuts import render
from django.db.models import Sum

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

def home(request):
    return render(request, 'home.html')  # This should match the template you want to show


def make_request(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_dashboard')  # Redirect to a success page
    else:
        form = BloodRequestForm()  # Initialize an empty form

    return render(request, 'myapp/makerequest.html', {'request_form': form})


def my_request(request):
    # Fetch all blood requests (modify as needed, e.g., filtering by the user)
    makerequest = BloodRequest.objects.all()

    # Pass the blood requests to the template
    return render(request, 'myapp/my_request.html', {'makerequest': makerequest})

# Improved Dashboard View to show blood group count for donors
# def donor_dashboard(request):
#     if request.user.is_authenticated and hasattr(request.user, 'donor'):
#         # Get all donors and count blood groups
#         blood_groups = Donor.objects.values('blood_type').annotate(count=models.Count('blood_type'))
#         donor_data = {'blood_groups': blood_groups}

#         return render(request, 'myapp/donor_dashboard.html', donor_data)
#     else:
#         messages.error(request, 'You are not authorized to access this page.')
#         return redirect('home')

def donor_dashboard(request):
    if request.user.is_authenticated and hasattr(request.user, 'donor'):
        # Redirect to donate_blood page
        return redirect('donate_blood')  # Replace 'donate_blood' with the actual URL name
        
        # Alternatively, you can comment out the redirect if you want to show data first:
        # Get all donors and count blood groups
        blood_groups = Donor.objects.values('blood_type').annotate(count=models.Count('blood_type'))
        donor_data = {'blood_groups': blood_groups}
        
        # Render the donor_dashboard with donor data (if no redirection is applied)
        # return render(request, 'myapp/donor_dashboard.html', donor_data)
    else:
        # If not authenticated, redirect to the home page
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')

# Admin Dashboard View
def admin_dashboard(request):
    # Check if user is authenticated and a staff member
    if request.user.is_authenticated and request.user.is_staff:
        # Redirect to 'all_donor_history' page after login
        return redirect('all_donor_history')  # This will redirect the user to the all_donor_history page

    # If the user is not authenticated or is not staff, show error
    messages.error(request, 'You are not authorized to access this page.')
    return redirect('home')  
# Patient Dashboard View
def patient_dashboard(request):
    if request.user.is_authenticated and hasattr(request.user, 'patient'):
        # Automatically redirect to 'makerequest' view after rendering the dashboard
        return redirect('makerequest')  # Make sure 'makerequest' is the name of your URL pattern
        
    else:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')  # Redirect to

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
    """Handle blood donation submission."""
    if request.user.is_authenticated and hasattr(request.user, 'donor'):
        donation_form = forms.DonationForm(request.POST or None)
        if request.method == 'POST' and donation_form.is_valid():
            blood_donate = donation_form.save(commit=False)
            blood_donate.donor = Donor.objects.get(user=request.user)
            blood_donate.save()
            messages.success(request, 'Donation submitted successfully.')
            return redirect('donation_history')

        return render(request, 'myapp/donate_blood.html', {'donation_form': donation_form})

    messages.error(request, 'You must be logged in as a donor to donate blood.')
    return redirect('home')

def donation_history(request):
    """Render the donation history for donors."""
    if request.user.is_authenticated and hasattr(request.user, 'donor'):
        donor = Donor.objects.get(user=request.user)
        donations = BloodDonate.objects.filter(donor=donor)
        return render(request, 'myapp/donation_history.html', {'donations': donations})

    messages.error(request, 'You are not authorized to view this page.')
    return redirect('home')



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
    logout(request)
    return redirect('home')



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

def contact_us(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact_us')  # Redirect back to the same page after successful form submission
    else:
        form = ContactUsForm()
    
    return render(request, 'myapp/contact_us.html', {'form': form})

def all_donor_history(request):
    """View all donation histories for admin."""
    if request.user.is_authenticated and request.user.is_staff:
        donations = BloodDonate.objects.select_related('donor', 'donor__user').all()

        # Check if the form has been submitted and handle the status change temporarily
        if request.method == 'POST':
            updated_donations = []
            for donation in donations:
                # Get the status from the form data
                status = request.POST.get(f'status_{donation.id}')
                if status:
                    # Temporarily update the status in the context (without saving to the DB)
                    donation.status = status
                updated_donations.append(donation)

            # Pass the updated donations back to the template to reflect the changes
            donations = updated_donations
        
        return render(request, 'myapp/all_donor_history.html', {'donations': donations})
    
    messages.error(request, 'You are not authorized to access this page.')
    return redirect('home')

def all_patient_history(request):
    patients = Patient.objects.all()

    # Check if the form has been submitted and handle the status change temporarily
    if request.method == 'POST':
        # Create a list of updated patients with their temporary status changes
        updated_patients = []
        for patient in patients:
            status = request.POST.get(f'status_{patient.id}')
            if status:
                # Temporarily update the status in the context (without saving to the DB)
                patient.status = status
            updated_patients.append(patient)

        # Pass the updated patients back to the template to reflect the changes
        patients = updated_patients
    
    return render(request, 'myapp/all_patient_history.html', {'patients': patients})


def blood_stock_view(request):
    # Group by blood type and sum the units
    blood_stock = BloodDonate.objects.values('bloodgroup').annotate(total_units=Sum('unit')).order_by('bloodgroup')
    
    return render(request, 'myapp/blood_stock.html', {'blood_stock': blood_stock})

def update_request_status(request, model_type, request_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')

        # Check if status is valid
        valid_statuses = ['pending', 'approved', 'rejected']
        if new_status not in valid_statuses:
            return JsonResponse({"error": "Invalid status value"}, status=400)
        
        # Choose the appropriate model based on the type
        if model_type == "patient":
            request_instance = get_object_or_404(PatientRequest, id=request_id)
        elif model_type == "donate":
            request_instance = get_object_or_404(BloodDonate, id=request_id)
        else:
            return JsonResponse({"error": "Invalid model type. Expected 'patient' or 'donate'."}, status=400)

        # Update the status
        request_instance.status = new_status
        request_instance.save()

        # Return the updated status in the response
        return JsonResponse({"message": "Status updated successfully", "status": request_instance.status})
    
    return JsonResponse({"error": "Invalid request method. Only POST is allowed."}, status=405)

def update_donor_status(request, donation_id):
    """Update donation status."""
    if request.method == 'POST':
        data = json.loads(request.body)
        status = data.get('status')

        try:
            donation = BloodDonate.objects.get(id=donation_id)
            donation.status = status
            donation.save()  # Save the updated status
            print(f"Donation status updated: {donation.status}")  # Debug log
            return JsonResponse({'message': 'Donation status updated successfully.'})
        except BloodDonate.DoesNotExist:
            print(f"Donation with ID {donation_id} not found")  # Debug log
            return JsonResponse({'error': 'Donation not found.'}, status=404)