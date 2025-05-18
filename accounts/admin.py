from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


# Customize admin for CustomUser model.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm  # Form for adding users.
    form = CustomUserChangeForm        # Form for editing users.
    model = CustomUser                 # Associate with CustomUser model.
    list_display = ['username', 'email', 'first_name', 'last_name', 'birthdate', 'is_staff']  # Fields in user list.
    ordering = ('first_name', 'last_name')  # Default ordering.

    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'birthdate')}),
    )  # Fields on add user form.

    fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'last_name', 'birthdate')}),  # Basic info.
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )  # Fields on edit user form.

# Register CustomUser with the admin site.
admin.site.register(CustomUser, CustomUserAdmin)