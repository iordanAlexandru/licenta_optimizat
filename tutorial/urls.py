"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = "tutorial"
urlpatterns = [
    path('update/', views.pacient_create_view, name='website_update'),
    path('about/', views.about, name='website_about'),
    path('pacient_details/', views.pacient_general_form_view, name='website_general_form'),
    path('register/', views.registerPage, name='website_registerPage'),
    path('login/', views.loginPage, name='website_loginPage'),
    path('', views.index, name='website_index'),
    path('logout/', views.logoutPage, name='website_logoutPage'),
    path('results/', views.resultsView, name='website_results'),

 #   path('login/', LoginView.as_view(template_name='website/login.html'), name='website_login'),
]
