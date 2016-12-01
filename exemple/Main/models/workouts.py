from django.db import models

from Main.handlers.utilities import get_new_token
from Main.models.users import User
from Main.models.images import Image
from Main.models.exercises import Exercises

import json

		
class WorkoutType(models.Model):
	#####
	# Saves the Workout type
	#####
	name = models.TextField(max_length=32)

	enabled = models.BooleanField(default=True)
	
	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
	
	def get_as_short_dict(self):
		return {
			"name": self.name
		}

	class Meta:
		app_label = 'Main'
		
class WorkoutTarget(models.Model):
	#####
	# Saves the Workout target people
	#####
	name = models.TextField(max_length=32)
	
	enabled = models.BooleanField(default=True)
	
	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
	
	def get_as_short_dict(self):
		return {
			"name": self.name
		}

	class Meta:
		app_label = 'Main'
		
class Workout(models.Model):
	#####
	# Saves the Workout's information
	#####
	user = models.ForeignKey(User, null=True)
	#todo add gym here
	
	type = models.ForeignKey(WorkoutType)
	target = models.ForeignKey(WorkoutTarget)
	
	short_desc = models.TextField(max_length=64)
	long_desc = models.TextField(max_length=2048)
	
	exercises = models.TextField(default="[]")
	
	views = models.IntegerField(default=0)
	
	enabled = models.BooleanField(default=True)
	
	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
	
	def get_as_short_dict(self):	
		return {
			"user": self.user.id,
			"type": self.type.get_as_short_dict(),
			"target": self.target.get_as_short_dict(),
			"short_desc": self.short_desc,
			"updated_at": str(self.updated_at)
		}
	
	def get_as_long_dict(self):
		# Loads the exercises info
		exercises_native = json.loads(self.exercises)
		
		# Gets the remaining info about the exercises
		exercises_retrieved = Exercises.objects.filter(id__in=exercises_native["id_list"])
		
		# Starts a empty dict to save the processed info
		exercises_dict = {}
		
		# Loops it
		for exercise in exercises_retrieved:
			# Added it to the empty dict
			exercises_dict.update({exercise.id: exercise.get_as_short_dict()})
			
		# Starts another empty dict to save the final info
		exercises_final = {}
		
		# Loops the dict already ordered
		for i in range(1, exercises_native["total"] + 1):
			# Gets the first part of the info
			tmp = exercises_native["exercises"][str(i)]
			
			# Addeds the remaining info to the temporary dict
			tmp.update(exercises_dict[tmp["id"]])
			
			# Addes the info to the final dict
			exercises_final.update({tmp["order"]: tmp})
	
		return {
			"user": self.user.id,
			"type": self.type.name,
			"target": self.target.name,
			"short_desc": self.short_desc,
			"long_desc": self.long_desc,
			"exercises": exercises_final,
			"updated_at": str(self.updated_at)
		}
		
	@staticmethod
	def validate_exercises(exercises, user_id):
		order_list = []
		
		exercises_counter = len(exercises)
		
		final = {
			"exercises": {},
			"total": exercises_counter,
			"id_list": []
		}
		
		for exercise in exercises:
			try:
				id = int(exercise["id"])
				order = int(exercise["order"])
				reps = int(exercise["reps"])
				sets = int(exercise["sets"])
			except:
				return False, None
			
			if order in order_list:
				return False, None
				
			order_list.append(order)
			
			if id not in final["id_list"]:
				final["id_list"].append(id)
		
			final["exercises"].update({order: {"id": id, "order": order, "reps": reps, "sets": sets}})
		
		try:
			tmp = UserExercises.objects.filter(user_id=user_id, id__in=final["id_list"]).count()
			if tmp == len(final["id_list"]):
				return True, final
			else:
				return False, None
		except:
			return False, None
			
			
	class Meta:
		app_label = 'Main'
		
class UserSubscribedWorkouts(models.Model):
	#####
	# Saves the Workouts user's subscribed to
	#####
	workout = models.ForeignKey(Workout)
	user = models.ForeignKey(User)
	
	enabled = models.BooleanField(default=True)
	
	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		app_label = 'Main'