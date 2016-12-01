from django.db import models

from Main.handlers.utilities import get_new_token
from Main.models.users import User


class Image(models.Model):
	#####
	# Saves the Images information
	#####
	
	# todo custom uuid for each image
	user = models.ForeignKey(User)

	versions = models.TextField()

	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	
	def get_as_short_dict(self):
		return {
			"versions": self.versions
		}

	class Meta:
		app_label = 'Main'