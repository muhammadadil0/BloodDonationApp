from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from . import models
from .models import BloodRequest, ContactUs

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['patient_name', 'patient_age', 'reason', 'blood_group', 'unit']
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'input--style-5'}),
            'patient_age': forms.NumberInput(attrs={'class': 'input--style-5'}),
            'reason': forms.Textarea(attrs={'class': 'input--style-5'}),
            'blood_group': forms.Select(attrs={'class': 'input--style-5'}),
            'unit': forms.NumberInput(attrs={'class': 'input--style-5'}),
        }
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
        label="Confirm Password"
    )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter a unique username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return password

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        return confirm_password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
        

class DonationForm(forms.ModelForm):
    class Meta:
        model = models.BloodDonate
        fields = ['age', 'bloodgroup', 'disease', 'unit']
        widgets = {
            'age': forms.NumberInput(attrs={'placeholder': 'Enter your age'}),
            'bloodgroup': forms.Select(attrs={'placeholder': 'Select blood group'}),
            'disease': forms.TextInput(attrs={'placeholder': 'Mention any diseases (if applicable)'}),
            'unit': forms.NumberInput(attrs={'placeholder': 'Enter blood units to donate'}),
        }

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }