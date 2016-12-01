from Main.API.endpoints.services.service import service
from Main.models.users import User, UserAuthKeys, UserAuthFails
from Main.forms.base import BaseIdForm, BaseUserIdForm
from Main.handlers.password import get_hash
from Main.handlers.utilities import get_remote_IP
from Main.handlers.email import send_email
from Main.forms.user import finish_register_0

from django.core.exceptions import ObjectDoesNotExist

import json

class api_user(service):
	class Meta:
		methods = ["GET", "PATCH", "POST"]
		requires_action = True
		requires_auth = True

	def get_user(self):

		form = BaseUserIdForm(self.getInputJson())

		if form.is_valid():

			try:
				user = User.objects.get(id=form.cleaned_data["id"])
			except ObjectDoesNotExist:
				return 400

			self.setResult({"user": user.get_as_small_dict()})

		else:
			self.addErrorJson(form.errors.as_json())
			print(form.errors.as_json())
			return 400

	def post_finish_register_0(self):

		form = finish_register_0(self.getInputJson())

		if form.is_valid():

			if self.user.finished_register == 0:
				self.user.first_name = form.cleaned_data["first_name"]
				self.user.last_name = form.cleaned_data["last_name"]
				self.user.country = form.cleaned_data["country"]
				self.user.finished_register = 1
				self.user.save()

			return 200

		else:
			self.addErrorJson(form.errors.as_json())
			print(form.errors.as_json())
			return 400

	# todo: add patch func