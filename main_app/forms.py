from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Sprint, Page, Task, Wireframe, Profile

TYPES = (
    ('client', 'Client'),
    ('dev', 'Developer')
)

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    email = forms.EmailField(max_length=25)
    user_type = forms.ChoiceField(choices=TYPES)

class ProjectForm(forms.ModelForm):
    client_email = forms.CharField(max_length=50)
    class Meta:
        model = Project
        fields = ['title']
        required = ['client_email']

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description']

class WireframeForm(forms.ModelForm):
    class Meta:
        model = Wireframe
        fields = ['image', 'description']

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['full_name', 'email']
