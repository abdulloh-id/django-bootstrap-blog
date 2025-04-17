from django import forms
from tinymce.widgets import TinyMCE
from .models import Article
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Hidden
from django_comments.forms import CommentForm as BaseCommentForm

class ArticleForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE())

    class Meta:
        model = Article
        fields = ['title', 'summary', 'body', 'photo']

class CrispyCommentForm(BaseCommentForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Explicitly define fields to exclude 'url'
        self.fields = {
            'content_type': self.fields['content_type'],
            'object_pk': self.fields['object_pk'],
            'timestamp': self.fields['timestamp'],
            'security_hash': self.fields['security_hash'],
            'comment': self.fields['comment'],
            'name': self.fields['name'],
            'email': self.fields['email'],
        }
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
            Submit('submit', 'Izoh Qoldirish', css_class='btn btn-success')
        )