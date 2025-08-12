from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomLoginForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # <-- Use request.FILES for file uploads
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            # MODIFIED: Redirect to login page instead of auto-login
            messages.success(request, f'Account created successfully for {username}! Please login with your credentials.')
            return redirect('users:login')  # Redirect to login page
            # END MODIFICATION
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# ADDED: Custom login view
class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'users/login.html'
    
    def get_success_url(self):
        return '/home/'  # Redirect to home after successful login
    
    def form_valid(self, form):
        messages.success(self.request, 'You have been logged in successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid email/username or password.')
        return super().form_invalid(form)

# Alternative function-based login view
def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('home')
        messages.error(request, 'Invalid email/username or password.')
    else:
        form = CustomLoginForm()
    return render(request, 'users/login.html', {'form': form})

