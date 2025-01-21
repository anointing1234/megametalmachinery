from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Account,PartnerRegistration
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
import re


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=100,
        help_text='Required. Add a valid email address'
    )
    username = forms.CharField(
        max_length=15
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        help_text='Required. Enter a password'
    )

    class Meta:
        model = Account
        fields = ("email", "username", "password")  # Include password field directly

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set Bootstrap classes and placeholders
        self.fields['email'].widget.attrs.update({
            'class': 'form-control form-control-bg',
            'style': 'border: 1px solid black;',
            'placeholder': 'Enter your email'
        })
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-bg',
            'style': 'border: 1px solid black;',
            'placeholder': 'Choose a username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control form-control-bg',
            'style': 'border: 1px solid black;',
            'placeholder': 'Create a password'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']

        if commit:
            user.set_password(self.cleaned_data['password'])  # Hash the password securely
            user.save()
        
        return user






class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control form-control-bg',
            'style': 'border: 1px solid black;',
            'placeholder': 'Enter your email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control form-control-bg',
            'style': 'border: 1px solid black;',
            'placeholder': 'Enter your password'
        })

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        # Authenticate with email and password
        user = authenticate(email=email, password=password)
        if user is None:
            raise forms.ValidationError("Invalid email or password.")
        self.user_cache = user
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

   

class PartnerRegistrationForm(forms.ModelForm):
    class Meta:
        model = PartnerRegistration
        fields = [
            'company_name',
            'contact_person',
            'email',
            'phone_number',
            'company_type',
            'address',
            'services_provided',
            'website',
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control form-control-bg',
                'style': 'border: 1px solid black;',
                'placeholder': 'Enter company name',
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control form-control-bg',
                'style': 'border: 1px solid black;',
                'placeholder': 'Enter contact person name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-bg',
                'style': 'border: 1px solid black;',
                'placeholder': 'Enter email address',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control form-control-bg',
                'style': 'border: 1px solid black;',
                'placeholder': 'Enter phone number',
            }),
            'company_type': forms.Select(attrs={
                'class': 'form-control form-control-bg',
                'style': 'border: 1px solid black;',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control form-control-bg',
                'style': 'border: 1px solid black;',
                'rows': 3,
                'placeholder': 'Enter company address',
            }),
            'services_provided': forms.Textarea(attrs={
                'class': 'form-control form-control-bg',
                'style': 'border: 1px solid black;',
                'rows': 4,
                'placeholder': 'Describe services provided',
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control form-control-bg',
                'style': 'border: 1px solid black;',
                'placeholder': 'Enter website URL (optional)',
            }),
        }

    