from django import forms
from testApp.models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    telefon = forms.CharField(required=True)
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', "first_name", "last_name", "telefon"]
    