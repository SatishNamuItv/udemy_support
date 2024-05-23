# views.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Course  # Assuming you have a Course model
from django.contrib.auth.models import User, Group

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admins').exists()

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
@user_passes_test(is_admin)
def manage_mentors(request):
    mentors = User.objects.filter(groups__name='Mentors')
    return render(request, 'manage_mentors.html', {'mentors': mentors})

@login_required
@user_passes_test(is_admin)
def manage_courses(request):
    courses = Course.objects.all()
    return render(request, 'manage_courses.html', {'courses': courses})

# Additional views for creating, updating, and deleting mentors and courses can be added similarly
from .forms import MentorForm

@login_required
@user_passes_test(is_admin)
def create_mentor(request):
    if request.method == 'POST':
        form = MentorForm(request.POST)
        if form.is_valid():
            mentor = form.save(commit=False)
            mentor.set_password(form.cleaned_data['password'])  # Hash the password
            mentor.save()
            mentor.groups.add(Group.objects.get(name='Mentors'))
            return redirect('manage_mentors')
    else:
        form = MentorForm()
    return render(request, 'create_mentor.html', {'form': form})