from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, FileInput, Select, EmailInput, PasswordInput


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username':   TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name':   TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name':   TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email':   EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
        }
