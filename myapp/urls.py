from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('login', views.logIn),
    path('register', views.register),
    path('logout', views.logOut),

    path('dashboard', views.dashboard),
    path('manual', views.manual),

    path('predict', views.handlePredict),
    path('csv', views.csvUpload),
]
