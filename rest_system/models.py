from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.conf import settings

from datetime import datetime, timedelta

from rest_system.utilities import get_new_big_token, get_new_token

User = settings.AUTH_USER_MODEL

class UserAuthKeys(models.Model):
	#####
	# Saves the Authentication Keys for Users, to use on remote environments like Mobile and FrontEnd
	#####
	user = models.ForeignKey(User)
	key = models.TextField(max_length=128, unique=True)
	ip = models.GenericIPAddressField()
	last_use = models.DateTimeField(auto_now_add=False, auto_now=True)
	expire_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

	def generate(self):
		self.key = get_new_big_token()
		self.expire_at = timezone.now()+timedelta(days=14)
		self.save()

	def valid(self):
		if self.expire_at > timezone.now():
			return True
		else:
			return False

	class Meta:
		app_label = 'rest_system'

class UserAuthFails(models.Model):
	#####
	# Saves the Authentication fails for ips
	#####
	ip = models.GenericIPAddressField()
	user = models.ForeignKey(User, null=True)
	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

	class Meta:
		app_label = 'rest_system'