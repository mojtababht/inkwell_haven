from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from .models import User
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ['last_name', 'first_name']
    list_display = ['first_name', 'last_name', 'phone_no', 'is_superuser', 'is_staff', 'is_active', 'last_login', 'date_joined']
