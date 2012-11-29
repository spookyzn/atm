from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from Main.models import Metric

def index(request):
    return render_to_response('index.html', {})