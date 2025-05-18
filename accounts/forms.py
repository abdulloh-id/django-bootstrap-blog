from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser, Profile


# Form for creating new CustomUser instances.
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser  # Associate with the CustomUser model.
        fields = ('username', 'email', 'first_name', 'last_name', 'birthdate') # Include these fields in the form.

# Form for editing existing CustomUser instances.
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser  # Associate with the CustomUser model.
        fields = ('username', 'email', 'first_name', 'last_name', 'birthdate') # Include these fields for editing.

# Form for editing Profile model instances, specifically the 'avatar' field.
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile  # Associate with the Profile model.
        fields = ['avatar'] # Only include the 'avatar' field in this form.