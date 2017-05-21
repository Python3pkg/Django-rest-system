from django.conf import settings

from rest_system.models import UserAuthKeys, UserAuthFails

from django.utils.timezone import utc
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

import datetime
import json
import re

import importlib
api_endpoints = importlib.import_module(settings.REST_ENDPOINTS)

class manager:

	result = {
		"code": 500,
		"result": {},
		"errors": []
	}

	endpoint = None

	def getResult(self):
		return self.result

	def getCode(self):
		return self.result["code"]

	def setCode(self, code):
		self.result["code"] = code

	def addError(self, error):
		self.result["errors"].append(error)

	def __init__(self, request, endpoint, action):
		self.result = {
			"code": 500,
			"result": {},
			"errors": []
		}

		tmp_callback = request.GET.get('callback', None)
		if tmp_callback:
			self.result["callback"] = tmp_callback

		self.setCode(self.process(request, endpoint, action))

	def process(self, request, endpoint, action):
		if request.method == "OPTIONS":
			return 200
		try:
			self.endpoint = getattr(api_endpoints, str('api_' + endpoint))(request, action)
		except ValueError:
			self.addError("not found")
			return 404
		else:
			if request.method not in self.endpoint.getMethods():
				return 405

			# checks if the endpoint requires auth
			if self.endpoint.requires_auth():
				a = request.META
				try:
					authkey = request.META['HTTP_AUTHORIZATION_1'] + request.META['HTTP_AUTHORIZATION_2']
				except:
					return 401

				if authkey != "":
				# Try to get the auth key
					try:
						keymodel = UserAuthKeys.objects.get(key=authkey)
					except ObjectDoesNotExist:
						return 401

					if keymodel.valid():
						self.endpoint.setUser(keymodel.user)
					else:
						return 406

				# User is not authenticated
				else:
					return 401

			if self.endpoint.requires_action() and action == "":
				self.addError("Action required")
				return 400

			self.endpoint.process()

			response = self.endpoint.getResult()

			if settings.DEBUG:
				print((json.dumps(response)))

			self.result["result"] = response["result"]
			self.result["errors"] = self.result["errors"] + response["errors"]

			return response["code"]