from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from tsl_assessment import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text 
from django.contrib.auth import authenticate, login,  logout
from . tokens import generate_token

from .models import Tweet
# from django.core.mail import send_mail

# Create your views here.
def home(request, *args, **kwargs): 
    return HttpResponse("<h1> Hello World <h1>")
    return render(request, "the_wall/index.html")

def tweet_detail_view(request, tweet_id, *args, **kwargs): 
    try:
        obj = Tweet.objects.get(id=tweet_id)
    except:
        raise Http404
    return HttpResponse("<h1> Hello {tweet_id} - {obj.content} <h1>")
 
def signup(request):
    
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists! Please try another username.")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('home')

        if len(username)>20:
            messages.error(request, "Username must be under 20 characters")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passwords don't match!")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username must be alpha-numeric")
            return redirect('home')

        myuser = User.objects.create_user (username, email, pass1)
        myuser.firstname = firstname 
        myuser.lastname = lastname 
        myuser.is_active = False
        myuser.save() 
        messages.success(request, "Your account has been created! We have sent you a confirmation email to confirm your identity.")


 
        #Welcome email 

        subject = "Welcome to The Wall"
        message = "Hello" + myuser.first_name + "! \n" + "Welcome to The Wall app. \n We've sent you a confirmation email to verify your identity and activate your account \n\n Thank you!." 
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        #Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your email @ The Wall Login"
        message2 = render_to_string('email_confirmation.html', {

            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
  
        return redirect('signin')


    return render(request, "the_wall/signup.html")

def activate(request, uidb64, token):
    try: 
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request, 'activation_failed.html')

def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, pass1=pass1) 

        if user is not None:
            login(request, user)
            firstname = user.first_name 
            return render(request, 'the_wall/index.html', {'firstname': firstname})

        else:
            messages.error(request, "Uh oh! Your username/password is incorrect.")
            return redirect('home')

    return render(request, "the_wall/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Sign Out success")
    return redirect('home') 



