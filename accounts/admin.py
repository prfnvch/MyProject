from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserRegistrationForm, CustomUserChangeForm
from .models import User
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = UserRegistrationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("username", "email", "first_name", "last_name", "date_of_birth", "avatar", "city", "country", "bio", "instagram", "telegram", "is_staff", "is_active")
    list_filter = ("username", "email", "first_name", "last_name", "date_of_birth", "avatar", "city", "country", "bio", "instagram", "telegram", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("username", "email", "first_name", "last_name", "date_of_birth", "avatar", "bookmarks", "city", "country", "follows", "bio", "instagram", "telegram", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "email", "first_name", "last_name", "date_of_birth", "avatar", "bookmarks", "city", "country", "bio", "follows", "instagram", "telegram", "password1", "password2", "is_staff",
                "is_active"
            )}
        ),
    )
    search_fields = ("username", "email")
    ordering = ("username", "email")


admin.site.register(User, CustomUserAdmin)
