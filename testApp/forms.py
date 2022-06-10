from django import forms
from testApp.models import *
from django_select2 import forms as s2forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class UsersForm(UserCreationForm):
    error_messages = {
        'password_mismatch': ('Parolele nu sunt identice.'),
    }
    email = forms.EmailField()
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'telefon']

class EditUsersForm(UserChangeForm):
    error_messages = {
        'password_mismatch': ('Parolele nu sunt identice.'),
    }
    password1 = forms.CharField(
        label=("Password1"),
        strip=False,
        required= False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    email = forms.EmailField()
    password = None
    class Meta:
        model = CustomUser
        fields = ['email', 'password1','first_name', 'last_name', 'telefon']
