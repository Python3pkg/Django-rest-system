from django.conf.urls import url
from rest_system.views import index_req, api_req

urlpatterns = [
    url(r'^$', index_req, name="api_index"),
    url(r'^(?P<endpoint>[a-z]+)/$', api_req, name="api"),
    url(r'^(?P<endpoint>[a-z]+)/(?P<action>[a-z0-9_-]+)/$', api_req, name="api"),
]
