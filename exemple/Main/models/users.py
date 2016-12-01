from django.db import models
from django.utils import timezone

from datetime import datetime, timedelta

from Main.handlers.utilities import get_new_big_token, get_new_token


class User(models.Model):
	#####
	# Saves the User information
	#####

	# Information required on register
	id = models.TextField(primary_key=True)
	username = models.TextField(max_length=16, unique=True)
	# Password is 24 Chars max
	password_hash = models.TextField(null=True)

	email = models.EmailField(max_length=24, unique=True)

	# Information required on first login
	first_name = models.TextField(null=True, max_length=32)
	last_name = models.TextField(null=True, max_length=32)
	gender = models.IntegerField(null=True)
	birthday = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
	country = models.TextField(max_length=2, null=True)

	finished_register = models.IntegerField(default=0)

	# Adicional Informaion
	profile_url = models.TextField(max_length=24, null=True)
	website = models.TextField(null=True)
	state = models.TextField(null=True)
	location = models.TextField(max_length=128, null=True)
	interests = models.TextField(max_length=128, null=True)

	# Information for internal use
	verified = models.BooleanField(default=False)
	private_profile = models.BooleanField(default=False)
	suspended_profile = models.BooleanField(default=False)

	# Email verification token
	activation_token = models.CharField(max_length=64, null=True)

	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

	def get_as_small_dict(self):
		return {
			"id": self.id,
			"name": str(self.first_name) + " " + str(self.last_name),
			"profile_url": self.profile_url,
			"verified": self.verified
		}

	def get_as_big_dict(self):
		return {
			"id": self.id,
			"name": str(self.first_name) + " " + str(self.last_name),
			"profile_url": self.profile_url,
			"verified": self.verified,
			"finished_register": self.finished_register,
			"created_at": str(self.created_at)
		}

	@staticmethod
	def generate(username, email):
		return {
			"id": get_new_token(),
			"username": username,
			"email": email,
			"activation_token": get_new_token()
		}

	class Meta:
		app_label = 'Main'

class UserAuthKeys(models.Model):
	#####
	# Saves the Authentication Keys for Users, to use on remote environments like Mobile
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
		app_label = 'Main'

class UserAuthFails(models.Model):
	#####
	# Saves the Authentication fails for ips
	#####
	ip = models.GenericIPAddressField()
	user = models.ForeignKey(User, null=True)
	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

	class Meta:
		app_label = 'Main'