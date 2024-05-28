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

    def __str__(self):
        return self.username

    
class Course(models.Model):
    udemy_course_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
