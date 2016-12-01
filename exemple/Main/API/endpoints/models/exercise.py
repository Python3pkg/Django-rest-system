from Main.API.endpoints.models.model import model
from Main.forms.feeds import newPost
from Main.handlers.password import get_hash
from Main.handlers.utilities import get_remote_IP
from Main.models.exercises import Exercises
from Main.forms.exercises import NewExercise
from Main.models.images import Image

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F

import json

class api_exercise(model):
	class Meta:
		methods = ["GET", "POST", "PATCH", "DELETE"]
		requires_action = False
		requires_auth = True

	def get_process(self):
	#####
	# Retrives all exercises created by the user
	#####

		exercises = Exercise.objects.filter(user=self.user, enabled=True)
			
		tmp = []
		for exercise in exercises:
			tmp.append(exercise.get_as_short_dict())
		
		self.setResult({"exercises": tmp})
		return 200

	def get_process_single(self, id):
	#####
	# Retrives a single exercise model
	#####
	
		try:
			id = int(id)
		except:
			return 400
		
		try:
			exercise = Exercise.objects.get(id=id, enabled=True)
		except ObjectDoesNotExist:
			return 401

		self.setResult({"exercise": exercise.get_as_long_dict()})
		return 200			

	def post_process(self):
	#####
	# Saves a new exercise
	#####

		form = NewExercise(self.getInputJson())

		if form.is_valid():
		
			try:
				image = Image.objects.get(id=form.cleaned_data["image"], enabled=True, user=self.user)
			except ObjectDoesNotExist:
				return 400
		
			exercise = Exercise.objects.create(
				user=self.user,
				name=form.cleaned_data["name"],
				desc=form.cleaned_data["desc"],
				image_id=form.cleaned_data["image"]
			)
			return 200

		else:
			self.addErrorJson(form.errors.as_json())
			print(form.errors.as_json())
			return 400

	def patch_process_single(self, id):
	#####
	# Updates a exercise
	#####
	
		form = NewExercise(self.getInputJson())

		if form.is_valid():
		
			try:
				image = Image.objects.get(id=form.cleaned_data["image"], enabled=True, user=self.user)
			except ObjectDoesNotExist:
				return 400
		
			try:
				exercise = Exercise.objects.get(id=id, user=self.user, enabled=True)
			except ObjectDoesNotExist:
				return 401
		
			exercise.name = form.cleaned_data["name"],
			exercise.desc = form.cleaned_data["desc"],
			exercise.image_id = form.cleaned_data["image"]
			
			return 200

		else:
			self.addErrorJson(form.errors.as_json())
			print(form.errors.as_json())
			return 400
			
	def delete_process_single(self, id):
	#####
	# Deletes a single exercise model
	#####
	
		try:
			clean_id = int(id)
		except:
			return 400
		
		try:
			exercise = Exercise.objects.get(id=clean_id, user=self.user, enabled=True)
		except ObjectDoesNotExist:
			return 401
			
		exercise.enabled = False
		exercise.save()
		
		return 200	