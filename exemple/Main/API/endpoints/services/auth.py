from Main.API.endpoints.services.service import service
from Main.models.users import User, UserAuthKeys, UserAuthFails
from Main.forms.auth import Login, Register, CheckUsername, Authkey, CheckActivate
from Main.handlers.password import get_hash
from Main.handlers.utilities import get_remote_IP
from Main.handlers.email import send_email

from django.core.exceptions import ObjectDoesNotExist

import json

class api_auth(service):
	class Meta:
		methods = ["POST", "DELETE"]
		requires_action = True
		requires_auth = False

	def post_login(self):

		form = Login(self.getInputJson())

		if form.is_valid():

			try:
				user = User.objects.get(username=form.cleaned_data["username"])
			except ObjectDoesNotExist:
				return 401

			phash = get_hash(form.cleaned_data["password"], user.id, user.created_at)

			if phash == user.password_hash:
				if user.activation_token != "":
					self.addError("Activate your account before login")
					# todo change code
					return 402
				if user.suspended_profile == True:
					self.addError("Your account has been suspended, please contact the support team for any questions")
					# todo change code
					return 403

				key = UserAuthKeys.objects.create(user=user, ip=get_remote_IP(self.request.META))
				key.generate()

				self.setResult({"key": key.key, "expire_at": str(key.expire_at)})
				return 200
			else:
				UserAuthFails.objects.create(user=user, ip=get_remote_IP(self.request.META))
				return 401

		else:
			self.addErrorJson(form.errors.as_json())
			print(form.errors.as_json())
			return 400

	def post_register(self):

		# TODO: add captcha
		form = Register(self.getInputJson())

		if form.is_valid():

			try:
				dic = User.generate(form.cleaned_data["username"], form.cleaned_data["email"])
				user = User.objects.create(**dic)
			except ObjectDoesNotExist:
				return 500
			print(user)
			phash = get_hash(form.cleaned_data["password"], user.id, user.created_at)
			user.password_hash = phash
			user.save()

			# TODO: change hardcoded url and email
			send_email("auth/register.html", "Wellcome", {"token": user.activation_token, "url": "http://that.g4brym.ovh:1234/#!/activate/?token=" + user.activation_token}, user.email)
			return 200

		else:
			self.addErrorJson(form.errors.as_json())
			print(form.errors.as_json())
			return 400

	def post_username(self):

		# TODO: add captcha
		form = CheckUsername(self.getInputJson())

		if form.is_valid():

			try:
				user = User.objects.get(username=form.cleaned_data["username"])
				return 409
			except ObjectDoesNotExist:
				return 202

		else:
			self.addErrorJson(form.errors.as_json())
			print(form.errors.as_json())
			return 400

	def post_activate(self):

		# TODO: add captcha
		form = CheckActivate(self.getInputJson())

		if form.is_valid():

			try:
				user = User.objects.get(activation_token=form.cleaned_data["token"])
			except ObjectDoesNotExist:
				return 406

			user.activation_token = ""
			user.save()

			return 200


		else:
			self.addErrorJson(form.errors.as_json())
			print(form.errors.as_json())
			return 400

	def delete_authkey(self):
		form = Authkey(self.getInputJson())

		if form.is_valid():

			try:
				key = UserAuthKeys.objects.get(key=form.cleaned_data["authkey"])
				key.delete()
				return 200
			except ObjectDoesNotExist:
				return 200

		else:
			self.addErrorJson(form.errors.as_json())
			print(form.errors.as_json())
			return 400

	def post_authkey(self):
		form = Authkey(self.getInputJson())

		if form.is_valid():

			try:
				key = UserAuthKeys.objects.get(key=form.cleaned_data["authkey"])
				self.setResult({"user": key.user.get_as_big_dict()})
				return 200
			except ObjectDoesNotExist:
				return 404

		else:
			self.addErrorJson(form.errors.as_json())
			print(form.errors.as_json())
			return 400