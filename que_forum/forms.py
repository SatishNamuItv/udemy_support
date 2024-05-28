# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('mentor', 'Mentor'),
]

class MentorForm(UserCreationForm):
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
