from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rooms import models as rooms_models
from . import models


class RoomInline(admin.StackedInline):

    model = rooms_models.Room


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    # inlines = (RoomInline,)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "super_hosts",
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("super_hosts",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "super_hosts",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
    )
