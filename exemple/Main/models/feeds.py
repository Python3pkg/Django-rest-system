from django.db import models

from Main.handlers.utilities import get_new_token
from Main.models.users import User

import json

class Post(models.Model):
	#####
	# Saves the Post's information
	#####
	user = models.ForeignKey(User)

	text = models.TextField(max_length=1024)
	tags = models.TextField(default="[]")
	link = models.TextField(max_length=128, null=True) # todo: change later to another model

	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		app_label = 'Main'

	def get_as_dict(self):
		return {
			"id": self.id,
			"user": self.user.id,
			"text": self.text,
			"tags": json.loads(self.tags),
			"link": self.link,
			"updated_at": str(self.updated_at),
			"created_at": str(self.created_at)
		}

	def get_as_long_dict(self, user_id):
		return {
			"id": self.id,
			"user": self.user.id,
			"text": self.text,
			"tags": json.loads(self.tags),
			"link": self.link,
			"updated_at": str(self.updated_at),
			"created_at": str(self.created_at),
			"has_awesome": Awesome.objects.filter(user_id=user_id, post_id=self.id, enabled=True).count(),
			"n_awesomes": Awesome.objects.filter(post_id=self.id, enabled=True).count(),
			"n_comments": 0 # TODO
		}

class Awesome(models.Model):
	#####
	# Saves the Awesome's information
	#####
	post = models.ForeignKey(Post)
	user = models.ForeignKey(User)

	enabled = models.BooleanField(default=True)

	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		app_label = 'Main'