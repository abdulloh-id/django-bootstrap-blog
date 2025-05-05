from django import forms
from tinymce.widgets import TinyMCE
from .models import Article, Category, Tag
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Hidden
from django_comments.forms import CommentForm as BaseCommentForm

class ArticleForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE())
    tag_input = forms.CharField(
        required=False, 
        label='Tags',
        help_text='Enter tags separated by commas (e.g., news, technology, django)',
        widget=forms.TextInput(attrs={'placeholder': 'tag1, tag2, tag3'})
    )

    class Meta:
        model = Article
        fields = ['title', 'summary', 'body', 'photo', 'category', 'tag_input']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        
        # If we're editing an existing article, populate the tag_input
        if instance:
            self.initial['tag_input'] = ', '.join([tag.name for tag in instance.tags.all()])

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            
            # Handle tags
            if 'tag_input' in self.cleaned_data and self.cleaned_data['tag_input']:
                # Clear existing tags
                instance.tags.clear()
                
                # Process each tag
                tag_names = [t.strip() for t in self.cleaned_data['tag_input'].split(',') if t.strip()]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name,
                        defaults={'slug': tag_name.lower().replace(' ', '-')}
                    )
                    instance.tags.add(tag)
                    
        return instance

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