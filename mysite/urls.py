from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login', views.logIn, name='login'),
    path('register', views.register, name='register'),


    path('signup', views.handleSignup, name='handleSignup'),
    path('signin', views.handleSignin, name='handleSignin'),
    path('signout', views.handleSignout, name='handleSignout'),

    path('dashboard', views.dashboard, name='dashboard'),

    path('manual', views.manual, name='manual'),
]
