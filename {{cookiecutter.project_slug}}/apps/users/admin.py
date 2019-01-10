from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (_("Personal info"), {"fields": ("username", "first_name", "last_name", "password")}),
        (_("Permissions"), {"fields": ("role", "is_active", "is_staff", "is_superuser")}),
        (_("Important dates"), {"fields": ("last_login", "created_at", "updated_at")}),
    )
    readonly_fields = ("last_login", "created_at", "updated_at")
    list_display = ("username", "last_login", "is_active", "is_staff", "is_superuser")
    search_fields = ("username",)
    list_filter = ("is_active", "is_staff", "is_superuser")
    ordering = ("username",)
    filter_horizontal = ()


admin.site.unregister(Group)
