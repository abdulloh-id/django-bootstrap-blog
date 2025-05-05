from django.contrib import admin
from .models import Article, Category, Tag
from django_comments.models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'comment', 'submit_date', 'is_removed')
    list_filter = ('is_removed', 'submit_date')
    search_fields = ('comment', 'user_name')

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'date')
    list_filter = ('category', 'date')
    search_fields = ('title', 'summary', 'body')
    filter_horizontal = ('tags',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)