from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from . import models


@admin.register(models.User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (_("Personal info"), {"fields": ("username", "email", "password")}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_confirmed", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (_("Important dates"), {"fields": ("last_login", "created_at", "updated_at")}),
    )
    readonly_fields = ("last_login", "created_at", "updated_at")
    list_display = ("username", "email", "last_login", "is_active", "is_confirmed", "is_staff", "is_superuser")
    search_fields = ("username", "email")
    list_filter = ("is_active", "is_confirmed", "is_staff", "is_superuser")
    ordering = ("username", "email")


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")
