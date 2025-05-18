from django.urls import path

from . import views

app_name = 'accounts'  # Namespace for URLs in this app.

urlpatterns = [
    path('profile/', views.edit_profile_view, name='edit_profile'),  # URL pattern for editing user profile.
    path('profile/change-password/', views.change_password, name='change_password'),  # URL pattern for changing user password.
]