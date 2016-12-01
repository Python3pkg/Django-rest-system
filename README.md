# Django-rest-system
Full rest system for Django, will help you save hundreds of lines

# Documentation
More coming soon

# Use case
## Retrive User information
With just 12 lines of code you can check if the request is authenticated, is not a crawler bot tring to steal all of you data and safely return DB information
```python
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
```