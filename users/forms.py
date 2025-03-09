from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'avatar']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar', 'phone_number','password']