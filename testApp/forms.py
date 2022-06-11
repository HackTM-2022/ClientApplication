from django import forms
from testApp.models import *
from django_select2 import forms as s2forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import uuid

class UsersForm(UserCreationForm):
    error_messages = {
        'password_mismatch': ('Parolele nu sunt identice.'),
    }
    email = forms.EmailField()
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'role', 'first_name', 'last_name', 'telefon']
        widgets = {
            "role": s2forms.Select2Widget(attrs={
                'data-placeholder': 'Selectează rolul',
                'data-minimum-input-length': '0',
                'data-minimum-results-for-search': '20'}),
        }

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
        fields = ['email', 'password1', 'role', 'first_name', 'last_name', 'telefon']
        widgets = {
            "role": s2forms.Select2Widget(attrs={
                'data-placeholder': 'Selectează rolul',
                'data-minimum-input-length': '0',
                'data-minimum-results-for-search': '20'}),
        }

class ReservationForm(forms.Form):
    bike_code = forms.UUIDField()

class BikeDataForm(forms.ModelForm):
    class Meta:
        model=BikeData
        fields = ['lat','lon','battery']
