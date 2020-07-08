from django.db import models
from django.contrib.auth.models import User

# Create your models here.

TYPES = (
    ('client', 'Client'),
    ('dev', 'Developer')
)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    user_type = models.CharField(max_length=10, choices=TYPES)

class Project(models.Model):
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="client")
    dev = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="dev")
    title = models.CharField(max_length=50)

class Page(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)

class Wireframe(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    image = models.ImageField()
    description = models.TextField(max_length=200)

class Sprint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class Task(models.Model):
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    description = models.TextField(max_length=200)
    completed = models.BooleanField(default=False)