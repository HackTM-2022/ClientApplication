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
from testApp.mixins import UserMixin, AdminMixin


# Create your views here.
import requests
# Environment variables
import environ

# DEBUG TEMPLATE
# <div id="django-debug" class="d-none"><pre>{% filter force_escape %}{% debug %}{% endfilter % </pre></div>


class HomeView(TemplateView):
    template_name = "home.html"


class RegisterBikeView(AdminMixin, ListView):
    template_name="registerBikeView.html"
    model=Bike
    paginate_by=10
    ordering = ['id']
    
    def get(self, request, *args, **kwargs):
        context = {}
        return super(RegisterBikeView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        bike = Bike()
        bike.save()
        return JsonResponse({"secret":bike.secret})

class RemoveBikeView(AdminMixin, DeleteView):
    model=Bike
    success_url = "../../"
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    def post(self,request, *args, **kwargs):
        return super(RemoveBikeView, self).post(request, *args, **kwargs)

class QRView(UserMixin,TemplateView):
    template_name = "qr.html"

# POST start-trip with bike_code secret
class CreateReservation(UserMixin,View):
    def post(self,request, *args, **kwargs):
        form = ReservationForm(self.request.POST)
        if form.is_valid():
            bkc = self.request.POST.get("bike_code")
            bk_queryset = Bike.objects.all().filter(secret=bkc).order_by("pk")
            if len(bk_queryset)>0:
                bk = bk_queryset[0]
                if self.request.user:
                    # Check for any other current trip for bike and user
                    if len(Reservation.objects.all().filter(bike=bk,active=True))==0:
                        if len(Reservation.objects.all().filter(user=self.request.user,active=True))==0:
                            res = Reservation(bike=bk,user=self.request.user,active=True)
                            res.save()
                        else:
                            return JsonResponse({"status":"error","info":"Another trip is active for user"})
                    else:
                        return JsonResponse({"status":"error","info":"Another trip is active for bike"})
                else:
                    return JsonResponse({"status":"error","info":"Wrong user"})
            else:
                return JsonResponse({"status":"error","info":"Wrong bike identifier"})
        else:
            return JsonResponse({"status":"error","info":"Wrong bike identifier"})

    def get(self, request, *args, **kwargs):
        raise Http404()

# POST bike-ping with bike_code lat lon battery
class ReceiveBikePing(View):
    def get(self, request, *args, **kwargs):
        raise Http404()
    def post(self, request, *args, **kwargs):
        form = BikeDataForm(self.request.POST)
        if form.is_valid():
            bkc = self.request.POST.get("bike_code")
            bk_queryset = Bike.objects.all().filter(secret=bkc).order_by("pk")
            if len(bk_queryset)>0:
                bk = bk_queryset[0]
                # Save the bike data
                bd = form.save()
                bd.bike = bk
                bd.save()
                # If a job is available, update
                res = Reservation.objects.all().filter(bike=bk,active=True)
                if len(res)>0:
                    return JsonResponse({"email": res.user.email, \
                                        "first_name":res.user.first_name, \
                                        "last_name":res.user.last_name})
        raise Http404()

# POST 
class EndReservation(UserMixin,View):
    def get(self, request, *args, **kwargs):
        raise Http404()
    def post(self, request, *args, **kwargs):
        user = self.request.user
        if user:
            res = Reservation.objects.all().filter(user=user,active=True)
            for el in res:
                el.active=False
                el.save()
                return JsonResponse({"status":"Ended trip"})
        raise Http404()

