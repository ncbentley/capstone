from django import forms
from django.contrib.auth.forms import UserCreationForm

TYPES = (
    ('client', 'Client'),
    ('dev', 'Developer')
)

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    email = forms.EmailField(max_length=25)
    user_type = forms.ChoiceField(choices=TYPES)
