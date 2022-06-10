from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import DetailView, TemplateView, CreateView, UpdateView, DeleteView, View
from django.views.generic.list import MultipleObjectMixin, ListView
from django.views.generic.detail import SingleObjectMixin
from django.core.exceptions import PermissionDenied
from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404, FileResponse, HttpResponseNotFound
from django.urls import reverse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie
from django.db.models import Q
from zipfile import ZipFile

from testApp.models import *
from testApp.forms import *
from testApp.mixins import UserMixin


# Create your views here.
import requests
# Environment variables
import environ

# DEBUG TEMPLATE
# <div id="django-debug" class="d-none"><pre>{% filter force_escape %}{% debug %}{% endfilter % </pre></div>

class HomeView(TemplateView):
    template_name = "home.html"
