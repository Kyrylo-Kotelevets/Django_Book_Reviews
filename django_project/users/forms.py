"""
Forms for Users App
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    """
    Django Form for User Model used for registration
    """

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class UserUpdateForm(forms.ModelForm):
    """
    Django Form for User Model used for updating data
    """

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email',)


class ProfileUpdateForm(forms.ModelForm):
    """
    Django Form for Profile Model used for updating data
    """

    class Meta:
        model = Profile
        fields = ('image',)
