from Main.models.users import User
from Main.models.workouts import Workout, WorkoutTarget, WorkoutType
from Main.models.exercises import Exercises
from Main.handlers.countries import get_country

from django import forms
from django.core.exceptions import ObjectDoesNotExist

import json


class finish_register_0(forms.Form):
	first_name = forms.CharField(min_length=2, max_length=16, strip=True)
	last_name = forms.CharField(min_length=2, max_length=16, strip=True)
	country = forms.CharField(min_length=2, max_length=3, strip=True)

	def clean_country(self):
		# todo: generate cached types and targets
		country = self.cleaned_data['country']

		tmp = get_country(country)

		if tmp != None:
			return country
		else:
			raise forms.ValidationError("Invalid country")