from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm      
    model = CustomUser               
    list_display = ['username', 'email', 'first_name', 'last_name', 'birthdate', 'is_staff']
    ordering = ('first_name', 'last_name')

    # Fields on add user form.
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'birthdate')}),
    )

    # Fields on edit user form.
    fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'last_name', 'birthdate')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

# Register CustomUser with the admin site.
admin.site.register(CustomUser, CustomUserAdmin)