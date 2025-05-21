from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser, Profile

# Form for creating new CustomUser instances (unchanged)
class CustomUserCreationForm(UserCreationForm):
    birthdate = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Birthdate'
    )

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate == '':
            return None
        return birthdate

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'birthdate')

# Form for editing user profiles on the regular site (excludes username)
class CustomUserChangeForm(UserChangeForm):
    birthdate = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Birthdate'
    )

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate == '':
            return None
        return birthdate

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'birthdate')  # Exclude username

# Form for editing Profile model (unchanged)
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']