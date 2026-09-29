from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class UserLoginForm(AuthenticationForm):
    pass

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            "avatar",
            "first_name",
            "last_name",
            "email",
            "bio",
        )