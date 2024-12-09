from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
	class Meta(UserCreationForm):
		model = CustomUser
		# User submits these fields
		fields = ('username', 'first_name', 'last_name', 'email', 'age')

class CustomUserChangeForm(UserChangeForm):
	class Meta(UserChangeForm):
		model = CustomUser
		# User can change these fields
		fields = ('username', 'first_name', 'last_name', 'email', 'age')

