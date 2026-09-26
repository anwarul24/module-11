from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "phone_number", "is_staff", "is_active", "date_joined")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email", "phone_number")
    fieldsets = UserAdmin.fieldsets + (
        ("Rental System Profile", {"fields": ("role", "phone_number", "profile_photo")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Rental System Profile", {"fields": ("role", "phone_number", "email")}),
    )
