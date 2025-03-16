from django.contrib import admin
from .models import Article
from django_comments.models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'comment', 'submit_date', 'is_removed')
    list_filter = ('is_removed', 'submit_date')
    search_fields = ('comment', 'user_name')

# Register your models here.
admin.site.register(Article)

