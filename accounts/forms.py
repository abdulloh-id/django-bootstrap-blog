from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile
from django.utils.translation import gettext_lazy as _


User = get_user_model() 

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = _(
            'Your password must contain at least 8 characters and cannot be '
            'entirely numeric, too similar to your personal info, or commonly used.'
        )
        self.fields['username'].help_text = _(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        error_messages = {
            'username': {
                'unique': _('This username is already taken. Please choose another.'),
            }
        }

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
        model = User
        fields = ('email', 'first_name', 'last_name', 'birthdate')
        
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']