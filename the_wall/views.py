from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
def home(request): 
    return render(request, "the_wall/index.html")

def signup(request):
    
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['first-name']
        lastname = request.POST['last-name']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['confirm-pass']

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = firstname 
        myuser.last_name = lastname 

        myuser.save()

        messages.success(request, "Your account has been created!")

        return redirect('login')

    return render(request, "the_wall/signup.html")

def login(request):
    return render(request, "the_wall/login.html")

def logout(request):
    pass