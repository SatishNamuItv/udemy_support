from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ADMIN = 'admin'
    MENTOR = 'mentor'
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (MENTOR, 'Mentor'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=MENTOR)

    class Meta:
        db_table = 'customusers'

    def __str__(self):
        return self.username

    
class Course(models.Model):
    __tablename__ = 'courses'
    udemy_course_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'courses'

    def __str__(self):
        return self.title


class MentorCourseAssignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='mentor_course_assignments')
    mentor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mentor_course_assignments', limit_choices_to={'role': CustomUser.MENTOR})
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mentor_course_assignments'
    
    def __str__(self):
        return f"{self.mentor.username} -> {self.course.title}"