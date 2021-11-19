from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,  logout


# Create your views here.
def home(request): 
    return render(request, "the_wall/index.html")

def signup(request):
    
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser = User.objects.create_user (username, email, pass1)
        myuser.firstname = firstname 
        myuser.lastname = lastname 

        myuser.save()

        messages.success(request, "Your account has been created!")

        return redirect('signin')

    return render(request, "the_wall/signup.html")

def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, pass1=pass1) 

        if user is not None:
            login(request, user)
            firstname = user.first_name 
            return render(request, 'the _wall/index.html', {'firstname': firstname})

        else:
            messages.error(request, "Uh oh! Your username/password is incorrect.")
            return redirect('home')

    return render(request, "the_wall/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Sign Out success")
    return redirect('home') 