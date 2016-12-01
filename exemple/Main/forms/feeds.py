from Main.models.users import User

from django import forms
from django.core.exceptions import ObjectDoesNotExist

import json
import re

class newPost(forms.Form):
    text = forms.CharField(max_length=1024, min_length=1)
    tags = forms.CharField(required=False, max_length=10)
    link = forms.CharField(required=False, max_length=10)

    def clean_text(self):

        return self.cleaned_data['text'].strip()

    def clean_tags(self):

        try:
            return json.dumps([tag.strip("#") for tag in self.cleaned_data['text'].strip().split() if tag.startswith("#")])
        except KeyError:
            return None

    def clean_link(self):

        try:
            return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@#.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', self.cleaned_data['text'].strip())[0]
        except (IndexError, KeyError):
            return None