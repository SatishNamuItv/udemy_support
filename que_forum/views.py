from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group, Permission
from .forms import MentorForm
from .models import Course, CustomUser, MentorCourseAssignment
from django.views.decorators.http import require_POST

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def manage_courses(request):
    query = request.GET.get('q')

    if request.user.role == CustomUser.ADMIN:
        # If the user is an admin, show all courses or filter by query
        if query:
            courses = Course.objects.filter(title__icontains=query)
        else:
            courses = Course.objects.all()
    elif request.user.role == CustomUser.MENTOR:
        # If the user is a mentor, show only courses assigned to them or filter by query
        if query:
            courses = MentorCourseAssignment.objects.filter(
                mentor=request.user,
                course__title__icontains=query
            ).select_related('course')
        else:
            courses = MentorCourseAssignment.objects.filter(
                mentor=request.user
            ).select_related('course')
    else:
        # For any other type of user, handle accordingly
        return render(request, 'error.html', {'message': 'You do not have permission to view this page.'})

    mentors = CustomUser.objects.filter(role=CustomUser.MENTOR)

    # Pass the actual Course objects to the template if the user is a mentor
    if request.user.role == CustomUser.MENTOR:
        courses = [assignment.course for assignment in courses]

    return render(request, 'manage_courses.html', {'courses': courses, 'mentors': mentors})


@require_POST
@login_required
@user_passes_test(lambda u: u.role == CustomUser.ADMIN)
def assign_mentor(request, course_id):
    q = request.GET.get('q', '')
    courses = Course.objects.all()

    if q:
        courses = courses.filter(title__icontains=q)

    mentors = CustomUser.objects.filter(role=CustomUser.MENTOR)
    context = {
        'courses': courses,
        'mentors': mentors,
    }
    course = get_object_or_404(Course, id=course_id)
    mentor_id = request.POST.get('mentor_id')
    if mentor_id:
        mentor = get_object_or_404(CustomUser, id=mentor_id, role=CustomUser.MENTOR)
        # Check if the mentor is already assigned to this course
        if not MentorCourseAssignment.objects.filter(course=course, mentor=mentor).exists():
            MentorCourseAssignment.objects.create(course=course, mentor=mentor)
    return render(request, 'manage_courses.html', context)

@login_required
def manage_mentors(request):
    if request.user.role == CustomUser.ADMIN:
        # Logic to manage mentors/admins
        return render(request, 'manage_mentors.html', {})
    else:
        return render(request, 'error.html')

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
