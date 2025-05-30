from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomUser, Profile


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "email",
        "phone",
        "is_superuser",
        "is_active",
        "is_verified",
    )
    list_filter = ("email", "is_superuser", "is_active", "is_verified")
    search_fields = ("email",)
    ordering = ("email",)
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    fieldsets = (
        (
            "Authentication",
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
        (
            "Groups Permissions",
            {
                "fields": ("groups", "user_permissions"),
            },
        ),
        (
            "Important Date",
            {
                "fields": ("last_login",),
            },
        ),
    )
    add_fieldsets = (
        (
            "Add User",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "phone",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
