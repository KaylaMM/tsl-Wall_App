from django.contrib import admin
from django.urls import path, re_path, include
from . import views

urlpatterns = [ 
    path('', views.home, name="home"),
    path('tweets/<int:tweet_id', views.tweet_detail_view, name="tweet_detail_view"),  
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"), 
    path('activate/<uidb64>/<token>', views.activate, name="activate")
] 