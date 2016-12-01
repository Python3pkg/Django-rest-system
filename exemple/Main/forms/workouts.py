from Main.models.users import User
from Main.models.workouts import Workout, WorkoutTarget, WorkoutType
from Main.models.exercises import Exercises

from django import forms
from django.core.exceptions import ObjectDoesNotExist

import json


class NewWorkout(forms.Form):
	type = forms.IntegerField()
	target = forms.IntegerField()
	short_desc = forms.CharField(max_length=64, strip=True)
	long_desc = forms.CharField(max_length=2048, strip=True)
	exercises = forms.CharField(strip=True)

	def clean_type(self):
		# todo: generate cached types and targets
		type = self.cleaned_data['type']
		
		try:
			WorkoutType.objects.get(id=type, enabled=True)
			return type
		except ObjectDoesNotExist:
			raise forms.ValidationError("Invalid workout type")

	def clean_target(self):
		# todo: generate cached types and targets
		target = self.cleaned_data['target']
		
		try:
			WorkoutTarget.objects.get(id=target, enabled=True)
			return target
		except ObjectDoesNotExist:
			raise forms.ValidationError("Invalid workout target")

	def clean_short_desc(self):
		short_desc = self.cleaned_data['short_desc']

		return short_desc

	def clean_long_desc(self):
		long_desc = self.cleaned_data['long_desc']

		return long_desc

	def clean_exercises(self):
		exercises = json.loads(self.cleaned_data['exercises'])
				
		return exercises
