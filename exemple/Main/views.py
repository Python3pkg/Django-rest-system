from django.template import RequestContext, Context, Template, loader
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, render_to_response
from django.conf import settings

import json
import re
import os

from Main.API.manager import manager

def index_req(request):
    return JsonResponse({"error": "not found"}, status=404)

def v1_req(request):
    return redirect('index')

@csrf_exempt
def api_req(request, endpoint, action=""):
    result = manager(request, str(endpoint), str(action))

    return JsonResponse(result.getResult(), status=result.getCode())

        # Old method
        #dict = {
        #    "callback": willCallback,
        #    "response": json.dumps(result.getResult())
        #}
        #return render(request, 'api_callback.html', dict, status=result.getCode(), content_type="application/json")