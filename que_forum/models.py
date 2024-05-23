from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('mentor', 'Mentor'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=6, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    url = models.URLField()
    is_paid = models.BooleanField(default=True)
    published_title = models.CharField(max_length=255)
    visible_instructors = models.ManyToManyField(Profile)

    def __str__(self):
        return self.title

class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created = models.DateTimeField()
    num_replies = models.IntegerField()
    num_follows = models.IntegerField()
    num_reply_upvotes = models.IntegerField()
    modified = models.DateTimeField()
    last_activity = models.DateTimeField()
    is_read = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    num_upvotes = models.IntegerField()

    def __str__(self):
        return self.title

class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField()
    last_activity = models.DateTimeField()
    body = models.TextField()
    is_top_answer = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer to {self.question.title} by {self.user.user.username}"
