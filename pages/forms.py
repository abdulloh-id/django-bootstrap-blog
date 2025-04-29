# forms.py
from django import forms
from tinymce.widgets import TinyMCE
from .models import AboutPage

class AboutPageForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE())

    class Meta:
        model = AboutPage
        fields = ['photo', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].required = False