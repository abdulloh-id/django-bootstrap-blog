from django import forms
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

from .models import AboutPage


class AboutPageForm(forms.ModelForm):
    class Meta:
        model = AboutPage
        fields = ['photo', 'body']
        
        # Переносим разметку лейблов сюда
        labels = {
            'photo': _('Profile Photo'),
            'body': _('About Content'),
        }
        # Переносим виджет TinyMCE сюда, чтобы не ломать labels
        widgets = {
            'body': TinyMCE(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].required = False

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)