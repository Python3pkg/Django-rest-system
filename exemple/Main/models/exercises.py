from django.db import models

from Main.handlers.utilities import get_new_token
from Main.models.users import User
from Main.models.images import Image

import json


class Exercises(models.Model):
	#####
	# Saves the Exercises information
	#####
	user = models.ForeignKey(User)
	
	name = models.TextField(max_length=32)
	desc = models.TextField(max_length=128)
	image = models.ForeignKey(Image, null=True)

	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

	def get_as_short_dict(self):
	
		try:
			img_dict = self.image.get_as_short_dict()
		except AttributeError:
			img_dict = None
			
		return {
			"name": self.name,
			"desc": self.desc,
			"image": img_dict,
			"updated_at": str(self.updated_at)
		}

	def get_as_long_dict(self):
	
		try:
			img_dict = self.image.get_as_short_dict()
		except AttributeError:
			img_dict = None
			
		return {
			"name": self.name,
			"desc": self.desc,
			"image": img_dict,
			"updated_at": str(self.updated_at)
		}

	@staticmethod
	def build_exercise(id, order, reps=0, sets=0):
		return {
			"id": id,
			"order": order,
			"reps": reps,
			"sets": sets
		}

	@staticmethod
	def validate_exercise(exercise, user_id):
		try:
			tmp_1 = int(exercise["id"])
			tmp_2 = int(exercise["order"])
			tmp_3 = int(exercise["reps"])
			tmp_4 = int(exercise["sets"])
			UserExercises.objects.get(user_id=user_id, id=exercise["ids"])
			return True
		except:
			return False
	
	class Meta:
		app_label = 'Main'