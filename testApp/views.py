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
import re

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

class RegisterBikeView(UserMixin, View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    def is_local_ip(self, request):
        return re.search("^(10|127|169\.254|172\.1[6-9]|172\.2[0-9]|172\.3[0-1]|192\.168)\.",self.get_client_ip(request))
    def get(self, request, *args, **kwargs):
        return JsonResponse({"status":"working","is_local_ip":self.is_local_ip(request)}, status=200)

# class CreatePlan(UserMixin,CreateView):
#     form_class = PlanForm
#     model = Plan
#     template_name = "createPlan.html"
#     success_url = "../"

#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         if form.is_valid():
#             self.object = form.save()
#         else:
#             return self.form_invalid(form)

#     def get_context_data(self, **kwargs):
#         context=super().get_context_data(**kwargs)
#         #context["form_operatie"]=OperatieForm()
#         return context
    
#     def form_invalid(self, request, *args, **kwargs):
#         raise Http404()
    

class TmpConfirm(UserMixin,TemplateView):
    template_name="tmp.html"
# class Addtmp(UserMixin,CreateView):
#     model = Operatie
#     form_class = OperatieForm
#     def get(self, request, *args, **kwargs):
#         raise Http404()
#     # def post(self, request, *args, **kwargs):
#     #     self.object = None
#     #     tempdict = self.request.POST.copy()
#     #     tempdict['obj'] = Obj.objects.get(pk=tempdict['obj'])
#     #     form = self.form_class(tempdict)
#     #     breakpoint()
#     #     if form.is_valid():
#     #         return self.form_valid(form)
#     #     else:
#     #         return self.form_invalid(form)
#     def form_valid(self, form):
#         self.object = form.save()
#         return HttpResponse(200)
#     def form_invalid(self, form):
#         return HttpResponse(400)