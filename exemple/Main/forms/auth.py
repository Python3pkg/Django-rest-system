from Main.models.users import User

from django import forms
from django.core.exceptions import ObjectDoesNotExist

class Login(forms.Form):
    username = forms.CharField(max_length=16, min_length=3)
    password = forms.CharField(max_length=24, min_length=6)

    def clean_username(self):
        username = self.cleaned_data['username'].strip().capitalize()

        return username

    def clean_password(self):
        password = self.cleaned_data['password'].strip()

        return password

class CheckUsername(forms.Form):
    username = forms.CharField(max_length=16)

    def clean_username(self):
        username = self.cleaned_data['username'].strip().capitalize()

        return username

class CheckActivate(forms.Form):
    token = forms.CharField(min_length=64)

    def clean_token(self):
        token = self.cleaned_data['token'].strip()

        return token

class Authkey(forms.Form):
    authkey = forms.CharField(min_length=128)

class Register(forms.Form):
    username = forms.CharField(min_length=3, max_length=16)
    email = forms.EmailField(min_length=6, max_length=24)
    password = forms.CharField(min_length=6, max_length=24)
    password_confirm = forms.CharField(min_length=6, max_length=24)

    def clean_username(self):
        username = self.cleaned_data['username'].strip().capitalize()

        try:
            query = User.objects.get(username=username)
            raise forms.ValidationError("Username already in use")
        except ObjectDoesNotExist:
            return username

        return username

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        try:
            query = User.objects.get(email=email)
            raise forms.ValidationError("Email already in use")
        except ObjectDoesNotExist:
            return email

        return email

    def clean_password(self):
        password = self.cleaned_data['password'].strip()

        return password


    def clean_password_confirm(self):
        password = self.cleaned_data['password'].strip()
        password_confirm = self.cleaned_data['password_confirm'].strip()

        if password != password_confirm:
            raise forms.ValidationError("Passwords doesn't match")

        return password_confirm