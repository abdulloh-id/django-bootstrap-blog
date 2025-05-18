from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Hidden, Layout, Submit
from django import forms
from django_comments.forms import CommentForm as BaseCommentForm
from tinymce.widgets import TinyMCE

from .models import Article, Category, Tag


class ArticleForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE()) # Rich text editor.
    tag_input = forms.CharField(required=False, label='Tags', help_text='Comma-separated.',
                                widget=forms.TextInput(attrs={'placeholder': 'tag1, tag2, tag3'})) # Input for tags.

    class Meta:
        model = Article
        fields = ['title', 'summary', 'body', 'photo', 'category', 'tag_input'] # Form fields.

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if instance:
            self.initial['tag_input'] = ', '.join(t.name for t in instance.tags.all()) # Show existing tags.

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        if 'tag_input' in self.cleaned_data and self.cleaned_data['tag_input']:
            instance.tags.clear() # Remove old tags.
            tag_names = [t.strip() for t in self.cleaned_data['tag_input'].split(',') if t.strip()]
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name, defaults={'slug': name.lower().replace(' ', '-')})
                instance.tags.add(tag) # Add new tags.
        return instance

class CrispyCommentForm(BaseCommentForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = {f: self.fields[f] for f in ['content_type', 'object_pk', 'timestamp', 'security_hash', 'comment', 'name', 'email']} # Keep these.
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = 'comments-post-comment'
        self.helper.layout = Layout(
            Field('content_type'),
            Field('object_pk'),
            Field('timestamp'),
            Field('security_hash'),
            'comment',
            'name',
            'email',
            Submit('submit', 'Izoh Qoldirish', css_class='btn btn-success') # Submit button.
        )