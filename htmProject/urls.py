"""Mindhive URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from testApp import views as app_views
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView


urlpatterns = [
    path('django-admin/', admin.site.urls, name='django-admin'), # REMOVE IN PRODUCTION
    # Home page
    path('', app_views.HomeView.as_view(), name='home'),
    path('favicon.ico/', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico'))),
    path("register-bike/", app_views.RegisterBikeView.as_view(),name='register-bike'),
    path("register-bike/remove-bike/<int:pk>/", app_views.RemoveBikeView.as_view(),name='remove-bike'),
    path("start-trip/", app_views.CreateReservation.as_view(),name="start-trip"),
    path("end-trip/", app_views.EndReservation.as_view(),name="end-trip"),
    path("bike-ping/", app_views.ReceiveBikePing.as_view(),name="bike-ping"),
    path("current-location/", app_views.CurrentLocationView.as_view(),name="current-location"),

    # QR page
    path('qr/', app_views.QRView.as_view(), name="QR"),
    # Auth
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='users/change-password.html', success_url='../'), name="change-password"),
    # path('profile/', user_views.profile, name='profile'),
    
    # libs
    path("select2/", include("django_select2.urls")),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # REMOVE AFTER APACHE
