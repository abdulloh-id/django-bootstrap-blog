from django import forms
from tinymce.widgets import TinyMCE

from .models import AboutPage


class AboutPageForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE()) # Uses TinyMCE widget for rich text editing.

    class Meta:
        model = AboutPage # Links the form to the AboutPage model.
        fields = ['photo', 'body'] # Specifies the fields to include in the form.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].required = False # Makes the 'photo' field optional.