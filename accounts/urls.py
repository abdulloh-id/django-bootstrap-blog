# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.edit_profile_view, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    # You might already have other account-related URLs here
]