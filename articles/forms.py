import re

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Hidden, Layout, Submit
from django import forms
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_comments.forms import CommentForm as BaseCommentForm
from tinymce.widgets import TinyMCE

from .models import Article, Category, Tag


class ArticleForm(forms.ModelForm):
    body = forms.CharField(
        widget=TinyMCE(), 
        label=_('Body')
    )
    tag_input = forms.CharField(
        required=False, 
        label=_('Tags'), 
        help_text=_('Comma-separated.'),
        widget=forms.TextInput(attrs={'placeholder': _('tag1, tag2, tag3')})
    )

    class Meta:
        model = Article
        fields = ['title', 'summary', 'body', 'photo', 'category', 'tag_input']
        
        labels = {
            'title': _('Title'),
            'summary': _('Summary'),
            'photo': _('Thumbnail'),
            'category': _('Category'),
        }
            
    def clean_body(self):
        body = self.cleaned_data.get('body')
        if body:
            body = re.sub(r'<p[^>]*>(\s|&nbsp;|<br\s*/?>)*</p>', '', body)
            body = re.sub(r'<div[^>]*>(\s|&nbsp;|<br\s*/?>)*</div>', '', body)
            body = re.sub(r'<h[1-6][^>]*>(\s|&nbsp;)*</h[1-6]>', '', body)
            body = re.sub(r'(<br\s*/?>\s*){3,}', '<br><br>', body)
            body = re.sub(r'(&nbsp;\s*)+', ' ', body)
            body = re.sub(r'>\s+<', '><', body)
            body = re.sub(r'\s{2,}', ' ', body)
            body = body.strip()
            body = re.sub(r'^(<br\s*/?>\s*)+|(<br\s*/?>\s*)+$', '', body)
        return body

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        
        if instance and instance.pk:
            self.initial['tag_input'] = ', '.join(t.name for t in instance.tags.all())

        if 'category' in self.fields:
            self.fields['category'].widget.attrs.update({
                'class': 'form-control',
                'style': 'height: calc(2.25rem + 2px);'
            })

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        if 'tag_input' in self.cleaned_data and self.cleaned_data['tag_input']:
            instance.tags.clear()
            tag_names = [t.strip() for t in self.cleaned_data['tag_input'].split(',') if t.strip()]
            for name in tag_names:
                slug = slugify(name)
                tag, created = Tag.objects.get_or_create(name=name, defaults={'slug': slug})
                instance.tags.add(tag)
        return instance


class CrispyCommentForm(BaseCommentForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = {f: self.fields[f] for f in ['content_type', 'object_pk', 'timestamp', 'security_hash', 'comment', 'name', 'email']}
        
        self.fields['comment'].label = _('Comment')
        self.fields['name'].label = _('Name')
        self.fields['email'].label = _('Email')
        
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
            Submit('submit', _('Submit Comment'), css_class='btn btn-success')
        )