from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class PasswordResetForm(forms.Form):
    email = forms.EmailField()

class PasswordForgotFrom(UserCreationForm):

    class Meta:
        model = User
        fields = ['password1', 'password2']

class OldPasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())



