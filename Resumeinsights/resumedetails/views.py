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




BASE_DIR = Path(__file__).resolve().parent.parent


# Helper function to get file extension
def get_file_extension(file_name):
    return os.path.splitext(file_name)[1].lower()



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



# Function to check if the uploaded resume is ATS-friendly
def is_ats_friendly(url, name):
    # Construct the full path to the file in the 'uploads' folder
    absolute_url = os.path.join(settings.BASE_DIR, 'uploads', name)

    keyword = ['skills', 'education', 'certifications', 'experience', 'projects', 'awards', 'linkedin', 'languages']
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

    return rating, missing



# View to handle ATS analysis and show results
def analyzer(request):
    # Retrieve stored file details from session
    url = urllib.parse.unquote(request.session.get('url'))
    name = request.session.get('name')

    # Perform ATS analysis
    rating, missing = is_ats_friendly(url, name)

    # Prepare context for result display
    context = {
        'url': request.session.get('url'),
        'rating': rating,
        'missing': missing
    }
    
    return render(request, 'ats.html', context)  # Render ATS result page
