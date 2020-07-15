from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

TYPES = (
    ('client', 'Client'),
    ('dev', 'Developer')
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    user_type = models.CharField(max_length=10, choices=TYPES)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Project(models.Model):
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="client", null=True)
    dev = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="dev")
    title = models.CharField(max_length=50)

class Page(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)

class Wireframe(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='wireframe_images/')
    description = models.TextField(max_length=200)

class Sprint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    @property
    def completed(self):
        tasks = self.task_set.all()
        for task in tasks:
            if not task.completed:
                return False
        return True

class Task(models.Model):
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    description = models.TextField(max_length=200)
    completed = models.BooleanField(default=False)