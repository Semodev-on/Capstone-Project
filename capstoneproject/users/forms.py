from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.shortcuts import render, redirect
from django.contrib import messages

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    profile_picture = forms.ImageField(required=False)
    middle_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=True)
    gender = forms.ChoiceField(
        choices=[('', 'Select an option')] + CustomUser.GENDER_CHOICES,
        required=True
    )
    position = forms.ChoiceField(
        choices=[('', 'Select an option')] + CustomUser.POSITION_CHOICES,
        required=True
    )
    institutional_school = forms.CharField(max_length=255, required=True, label='Institutional (School)')
    contact_number = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'middle_name', 'last_name', 'gender', 'position',
                 'institutional_school', 'contact_number', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes and placeholders
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['middle_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Middle Name (Optional)'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        self.fields['position'].widget.attrs.update({'class': 'form-control'})
        self.fields['institutional_school'].widget.attrs.update({'class': 'form-control', 'placeholder': 'School/Institution'})
        self.fields['contact_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contact Number'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email Address'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Re-enter Password'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.middle_name = self.cleaned_data['middle_name']
        user.last_name = self.cleaned_data['last_name']
        user.gender = self.cleaned_data['gender']
        user.position = self.cleaned_data['position']
        user.institutional_school = self.cleaned_data['institutional_school']
        user.contact_number = self.cleaned_data['contact_number']
        if self.cleaned_data.get('profile_picture'):
            user.profile_picture = self.cleaned_data['profile_picture']
        if commit:
            user.save()
        return user

# ADDED: Custom login form
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email or Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
# END ADDITION

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # <-- Add request.FILES here
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('home')  # Redirect to home or login page
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

