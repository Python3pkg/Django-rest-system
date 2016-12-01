from Main.API.endpoints.models.model import model
from Main.forms.feeds import newPost
from Main.handlers.password import get_hash
from Main.handlers.utilities import get_remote_IP
from Main.models.workouts import Workout, UserSubscribedWorkouts
from Main.forms.workouts import NewWorkout
from Main.forms.base import BaseIdForm

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F

import json

class api_workout(model):
	class Meta:
		methods = ["GET", "POST", "PATCH", "DELETE"]
		requires_action = False
		requires_auth = True

	def get_process(self):
	#####
	# Retrives all workouts created by the user
	#####

		workouts = Workout.objects.filter(user=self.user, enabled=True)
			
		tmp = []
		for workout in workouts:
			tmp.append(workout.get_as_short_dict())
		
		self.setResult({"workouts": tmp})
		return 200

	def get_process_single(self, id):
	#####
	# Retrives a single workout model
	#####
	
		try:
			id = int(id)
		except:
			return 400
		
		try:
			workout = Workout.objects.get(id=id, enabled=True)
		except ObjectDoesNotExist:
			return 401
			
		workout.views=F('views') + 1
		workout.save()

		self.setResult({"workout": workout.get_as_long_dict()})
		return 200			

	def post_process(self):
	#####
	# Saves a new workout
	#####

		form = NewWorkout(self.getInputJson())

		if form.is_valid():

			valid, exercises = Workout.validate_exercises(form.cleaned_data["exercises"], self.user.id)
			
			if valid:
		
				workout = Workout.objects.create(
					user=self.user,
					type_id=form.cleaned_data["type"],
					target_id=form.cleaned_data["target"],
					short_desc=form.cleaned_data["short_desc"],
					long_desc=form.cleaned_data["long_desc"],
					exercises=json.dumps(exercises)
				)
				return 200
				
			else:
				return 400

		else:
			self.addErrorJson(form.errors.as_json())
			print(form.errors.as_json())
			return 400

	def patch_process_single(self, id):
	#####
	# Updates a workout
	#####

		form = NewWorkout(self.getInputJson())

		if form.is_valid():
		
			try:
				clean_id = int(id)
			except:
				return 400
				
			try:
				workout = Workout.objects.get(id=clean_id, user=self.user, enabled=True)
			except ObjectDoesNotExist:
				return 404
			
			workout.type=form.cleaned_data["type"]
			workout.target=form.cleaned_data["target"]
			workout.short_desc=form.cleaned_data["short_desc"]
			workout.long_desc=form.cleaned_data["long_desc"]
			workout.exercises=json.dumps(form.cleaned_data["exercises"])
			workout.save()
			
			return 200

		else:
			self.addErrorJson(form.errors.as_json())
			print(form.errors.as_json())
			return 400
			
	def delete_process_single(self, id):
	#####
	# Deletes a single workout model
	#####
	
		try:
			clean_id = int(id)
		except:
			return 400
		
		try:
			workout = Workout.objects.get(id=clean_id, user=self.user, enabled=True)
		except ObjectDoesNotExist:
			return 401
			
		workout.enabled = False
		workout.save()
		
		return 200	
			
	def get_subscribe(self):
	#####
	# Returns all subscribed workouts
	#####
	
		subscribed = UserSubscribedWorkouts.objects.filter(user=self.user, enabled=True).values_list('workout', flat=True)

		workouts = Workout.objects.filter(id__in=subscribed)
			
		tmp = []
		for workout in workouts:
			tmp.append(workout.get_as_short_dict())
		
		self.setResult({"workouts": tmp})
		return 200
			
	def post_subscribe(self):
	#####
	# Subscribe to a new workout
	#####

		form = BaseIdForm(self.getInputJson())

		if form.is_valid():

			try:
				workout = Workout.objects.get(id=form.cleaned_data["id"])
			except ObjectDoesNotExist:
				return 404

			object, created = UserSubscribedWorkouts.objects.get_or_create(user=self.user, workout_id=form.cleaned_data["id"])
			if not created:
				if object.enabled == True:
					object.enabled = False
					object.save()
					# todo change to a real code
					# Unsubscribed
					return 202
				else:
					object.enabled = True
					object.save()
					# Subscribed
					return 201
			return 201

		else:
			self.addError(form.errors.as_json())
			print(form.errors.as_json())
			return 400