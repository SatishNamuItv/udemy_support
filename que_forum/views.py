from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group, Permission
from .forms import MentorForm
from .models import Course, CustomUser

@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def manage_courses(request):
    if request.user.role == CustomUser.ADMIN:
        # If the user is an admin, show all courses
        courses = Course.objects.all()
    elif request.user.role == CustomUser.MENTOR:
        # If the user is a mentor, show only courses assigned to them
        courses = Course.objects.filter(mentor=request.user)
    else:
        # For any other type of user, handle accordingly
        # For example, you can redirect them to a different page or show an error message
        return render(request, 'error.html', {'message': 'You do not have permission to view this page.'})
    
    return render(request, 'manage_courses.html', {'courses': courses})

@login_required
def manage_mentors(request):
    if request.user.role == CustomUser.ADMIN:
        # Logic to manage mentors/admins
        # For example, you can list all users and provide options to set their roles
        return render(request, 'manage_mentors.html', {})
    else:
        return render(request, 'error.html', {'message': 'You do not have permission to view this page.'})

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
