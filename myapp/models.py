from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Helper function to validate age
def validate_age(value):
    if value < 18 or value > 120:
        raise ValidationError('Age must be between 18 and 120.')

class Patient(models.Model):
    # Link each Patient to a User instance
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Removed null=True and blank=True to ensure each Patient has a linked user
    blood_type = models.CharField(max_length=3)  # Store blood type
    contact_number = models.CharField(max_length=15)  # Store contact number
    address = models.TextField(blank=True, null=True)  # Store address, optional field
    age = models.IntegerField(validators=[validate_age])  # Age of the patient, validated
    date_of_birth = models.DateField(null=True, blank=True)  # Optional: add date of birth
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True, blank=True)  # Optional gender field

    def __str__(self):
        # Return the full name of the patient using first and last name from User model or their username
        return f"{self.user.first_name} {self.user.last_name}" if self.user.first_name and self.user.last_name else f"Unnamed Patient ({self.user.username})"

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'


class Donor(models.Model):
    # Link each Donor to a User instance
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Removed null=True and blank=True to ensure each Donor has a linked user
    blood_type = models.CharField(max_length=3)  # Store blood type
    contact_number = models.CharField(max_length=15)  # Store contact number
    address = models.TextField(blank=True, null=True)  # Store address, optional field
    age = models.IntegerField(validators=[validate_age])  # Age of the donor, validated
    donation_date = models.DateField(null=True, blank=True)  # Date of donation, optional

    def __str__(self):
        # Return the full name of the donor using first and last name from User model or their username
        return f"{self.user.first_name} {self.user.last_name}" if self.user.first_name and self.user.last_name else f"Unnamed Donor ({self.user.username})"

    class Meta:
        verbose_name = 'Donor'
        verbose_name_plural = 'Donors'
class PatientRequest(models.Model):
    patient_name = models.CharField(max_length=100)
    blood_type = models.CharField(max_length=5)  # A+, B+, etc.
    contact_number = models.CharField(max_length=15)
    status = models.CharField(max_length=20, default='pending')  # 'pending', 'approved'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.patient_name} for {self.blood_type} blood"
        
        
        
class BloodDonate(models.Model): 
    donor=models.ForeignKey(Donor,on_delete=models.CASCADE)   
    disease=models.CharField(max_length=100,default="Nothing")
    age=models.PositiveIntegerField()
    bloodgroup=models.CharField(max_length=10)
    unit=models.PositiveIntegerField(default=0)
    status=models.CharField(max_length=20,default="Pending")
    date=models.DateField(auto_now=True)
    def __str__(self):
        return self.donor
