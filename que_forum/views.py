from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group, Permission
from .forms import MentorForm
from .models import Course

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def manage_mentors(request):
    mentors = User.objects.filter(groups__name='Mentors')
    return render(request, 'manage_mentors.html', {'mentors': mentors})

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def manage_courses(request):
    courses = Course.objects.all()
    return render(request, 'manage_courses.html', {'courses': courses})

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def create_mentor(request):
    if request.method == 'POST':
        form = MentorForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Hash the password
            user.save()

            # Assign user to the appropriate group and set permissions based on the role
            role = form.cleaned_data['role']
            if role == 'admin':
                group, created = Group.objects.get_or_create(name='Admins')
                if created:
                    permissions = Permission.objects.all()  # Assign all permissions
                    group.permissions.set(permissions)
                user.groups.add(group)
                user.is_superuser = True  # Make user a superuser
                user.save()
            elif role == 'mentor':
                group, created = Group.objects.get_or_create(name='Mentors')
                user.groups.add(group)

            return redirect('manage_mentors')
    else:
        form = MentorForm()
    return render(request, 'create_mentor.html', {'form': form})
