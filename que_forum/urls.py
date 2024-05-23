from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name = 'home'),
    path('manage_mentors/', views.manage_mentors, name='manage_mentors'),
    path('manage_courses/', views.manage_courses, name='manage_courses'),
    path('create_mentor/', views.create_mentor, name = 'create_mentor')
]