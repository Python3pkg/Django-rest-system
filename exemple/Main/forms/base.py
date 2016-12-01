from Main.models.users import User

from django import forms
from django.core.exceptions import ObjectDoesNotExist

class BaseIdForm(forms.Form):
    id = forms.IntegerField()

class BaseUserIdForm(forms.Form):
    id = forms.CharField(min_length=32)