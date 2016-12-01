from Main.API.endpoints.services.service import service
from Main.models.users import User, UserAuthKeys, UserAuthFails
from Main.forms.auth import Login, Register, CheckUsername, Authkey
from Main.handlers.password import get_hash
from Main.handlers.utilities import get_remote_IP

from django.core.exceptions import ObjectDoesNotExist

import json

class api_image(service):
	class Meta:
		methods = ["POST"]
		requires_action = True
		requires_auth = True

	def post_upload(self):
		#todo
		return 200