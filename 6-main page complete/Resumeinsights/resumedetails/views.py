from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .models import Admin
# Create your views here.

def home(request):
    return render(request, 'index.html')

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        birth_date = request.POST.get('birth_date')

        try:
            # Check if the email already exists
            user = Admin.objects.get(email=email)
            messages.error(request, 'Email address already registered. Please use a different one.')
            return render(request, 'register.html')
        except Admin.DoesNotExist:
            user = Admin.objects.create_user(
                username=username,
                email=email,
                password=password,
                birth_date=birth_date
            )
            messages.success(request, 'Account created successfully')
            return redirect('login')

    return render(request, 'register.html')




def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate using the email field instead of username
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'login.html')

    return render(request, 'login.html')



def user_logout(request):
    logout(request)
    return redirect('index')


def ats(request):
    return render(request, 'ats.html')