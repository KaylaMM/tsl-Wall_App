from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request): 
    return render(request, "the_wall/index.html")

def signup(request):
    return render(request, "the_wall/signup.html")

def login(request):
    return render(request, "the_wall/login.html")

def logout(request):
    pass