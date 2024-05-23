from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings



class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    url = models.URLField()
    is_paid = models.BooleanField(default=True)
    published_title = models.CharField(max_length=255)
    visible_instructors = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'courses'

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
    
    class Meta:
        db_table = 'questions'

class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField()
    last_activity = models.DateTimeField()
    body = models.TextField()
    is_top_answer = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer to {self.question.title} by {self.user.username}"


    class Meta:
        db_table = 'answers'