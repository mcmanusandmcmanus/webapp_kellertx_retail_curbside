from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Curbside Profile",
            {
                "fields": (
                    "type",
                    "phone_number",
                )
            },
        ),
    )
    list_display = ("username", "email", "type", "is_staff")
    list_filter = ("type", "is_staff", "is_superuser")
