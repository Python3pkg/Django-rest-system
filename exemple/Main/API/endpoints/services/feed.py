from Main.API.endpoints.services.service import service
from Main.models.feeds import Post, Awesome
from Main.forms.feeds import newPost
from Main.forms.base import BaseIdForm
from Main.handlers.password import get_hash
from Main.handlers.utilities import get_remote_IP

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F

import json

class api_feed(service):
	class Meta:
		methods = ["GET", "POST", "DELETE"]
		requires_action = True
		requires_auth = True

	def get_posts(self):

		# todo: add form validation with BaseIdForm

		last_post_id = self.request.GET.get('last_post', None)

		if last_post_id == None:
			# todo: change later to get posts from friends
			posts = Post.objects.filter(user=self.user)[:20][::-1]

			tmp = []

			for post in posts:
				tmp.append(post.get_as_long_dict(self.user.id))

			self.setResult({"posts": tmp})

			return 200

		else:
			try:
				post_checker = Posts.objects.get(id=last_post_id)
			except ObjectDoesNotExist:
				return 400

			# todo: change later to get posts from friends
			posts = Post.objects.filter(id__gt=post_checker.id, user=self.user)[:20][::-1]

			tmp = []

			for post in posts:
				tmp.append(post.get_as_dict())

			self.setResult({"posts": tmp})

			return 200


	def post_post(self):

		form = newPost(self.getInputJson())

		if form.is_valid():
			post = Post.objects.create(user=self.user, text=form.cleaned_data["text"], tags=form.cleaned_data["tags"], link=form.cleaned_data["link"])

			self.setResult({"posts": [post.get_as_dict()]})

			return 200

		else:
			self.addError(form.errors.as_json())
			print(form.errors.as_json())
			return 400


	def post_awesome(self):

		form = BaseIdForm(self.getInputJson())

		if form.is_valid():

			try:
				post = Post.objects.get(id=form.cleaned_data["id"])
			except ObjectDoesNotExist:
				return 404

			object, created = Awesome.objects.get_or_create(user=self.user, post_id=form.cleaned_data["id"])
			counter = Awesome.objects.filter(post_id=form.cleaned_data["id"], enabled=True).count()
			if not created:
				if object.enabled == True:
					object.enabled = False
					object.save()
					self.setResult({"post_id": form.cleaned_data["id"], "counter": counter-1, "enabled": False})
					# Unawesome
					return 202
				else:
					object.enabled = True
					object.save()
					self.setResult({"post_id": form.cleaned_data["id"], "counter": counter+1, "enabled": True})
					# Awesomed
					return 201
			else:
				self.setResult({"post_id": form.cleaned_data["id"], "counter": counter, "enabled": True})
				# Awesomed
				return 201

		else:
			self.addError(form.errors.as_json())
			print(form.errors.as_json())
			return 400