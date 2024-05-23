"""
URL configuration for udemy_support project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# urls.py

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from que_forum import views
from authentication import views as login_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home', views.home, name='home'),
    path('manage_mentors/', views.manage_mentors, name='manage_mentors'),
    path('manage_courses/', views.manage_courses, name='manage_courses'),
    path('create_mentor/', views.create_mentor, name = 'create_mentor')
    # Additional paths for creating, updating, and deleting mentors and courses
]
