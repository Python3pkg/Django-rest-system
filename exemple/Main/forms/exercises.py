from Main.models.users import User
from Main.models.images import Image

from django import forms
from django.core.exceptions import ObjectDoesNotExist

import json


class NewExercise(forms.Form):
	name = forms.CharField(max_length=32, strip=True)
	desc = forms.CharField(max_length=128, strip=True)
	image = forms.CharField(max_length=64, required=False, strip=True)