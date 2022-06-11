from django.contrib import admin
from testApp.models import *
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

@admin.register(CustomUser)
class UserAdmin(DjangoUserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'role', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', "first_name", "last_name" 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'role')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ["secret",'code']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["id","user", "bike"]

@admin.register(BikeData)
class BikeDataAdmin(admin.ModelAdmin):
    list_display = ["bike","reservation","lat","lon","battery"]

