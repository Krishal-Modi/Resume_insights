from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .models import Admin
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.clickjacking import xframe_options_exempt
import os
from pathlib import Path
import urllib.parse
import PyPDF2
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


from django.core.mail import send_mail
from django.conf import settings

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

            # Send email upon successful registration
            send_mail(
                subject='Welcome to Resume Insights',
                message=f'Hi {username},\n\nThank you for registering at Resume Insights!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

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


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, "Your account has been deleted successfully.")
        return redirect("home")  # Redirect to the home page or another page after deletion
    return HttpResponseForbidden("Account deletion is only allowed through POST request.")



import os
import re
import urllib.parse
import PyPDF2
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

# Helper function to get file extension
def get_file_extension(file_name):
    return os.path.splitext(file_name)[1].lower()

# Function to extract email from text
def extract_email(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_pattern, text)
    return match.group(0) if match else None

# Function to extract phone number from text
def extract_phone_number(text):
    phone_pattern = r'\+?\d[\d -]{8,}\d'  # Regex for matching phone numbers
    match = re.search(phone_pattern, text)
    return match.group(0) if match else None

# View to handle file upload
@xframe_options_exempt
def upload_resume(request):
    context = {}
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        
        # Set the location for the FileSystemStorage to the 'uploads' folder
        fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'uploads'))  
        name = fs.save(uploaded_file.name, uploaded_file)  # Save the file in 'uploads' folder
        url = fs.url(name)

        file_extension = get_file_extension(name)
        os.chmod(os.path.join(settings.BASE_DIR, 'uploads', name), 0o777)  # Set permissions
        
        # Store file details in session for ATS analysis
        request.session['url'] = url
        request.session['name'] = name

        # Redirect to ATS analyzer after successful upload
        return redirect('analyzer')  # Redirect to the analyzer view
    
    return render(request, 'upload.html', context)

# Function to check if the uploaded resume is ATS-friendly and extract email and phone number
def is_ats_friendly(url, name):
    # Construct the full path to the file in the 'uploads' folder
    absolute_url = os.path.join(settings.BASE_DIR, 'uploads', name)

    keyword = ['skills', 'education', 'certifications', 'experience', 'projects', 'awards', 'linkedin', 'languages', 'courses', 'portfolio']
    missing = []
    rating = 0
    text_content = ""

    # Extract text from PDF using PyPDF2
    with open(absolute_url, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text_content += page.extract_text()

    # Lowercase the text to perform case-insensitive search
    text_content = text_content.lower()

    # Check for each keyword in the resume
    for i in keyword:
        if i in text_content:
            rating += 10
        else:
            missing.append(i)

    # Extract email address and phone number
    email_address = extract_email(text_content)
    phone_number = extract_phone_number(text_content)

    return rating, missing, email_address, phone_number  # Return phone number along with rating and missing keywords

# View to handle ATS analysis and show results
def analyzer(request):
    # Retrieve stored file details from session
    url = urllib.parse.unquote(request.session.get('url'))
    name = request.session.get('name')

    # Perform ATS analysis
    rating, missing, email_address, phone_number = is_ats_friendly(url, name)

    # Prepare context for result display
    context = {
        'url': request.session.get('url'),
        'rating': rating,
        'missing': missing,
        'email_address': email_address,  # Include email address in context
        'phone_number': phone_number      # Include phone number in context
    }
    
    return render(request, 'ats.html', context)  # Render ATS result page



def payment(request):
    return render(request, 'payment.html')