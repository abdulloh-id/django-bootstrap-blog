from django.contrib import admin
from django_comments.models import Comment

from .models import Article, Category, Tag


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'comment', 'submit_date', 'is_removed') # Displayed fields.
    list_filter = ('is_removed', 'submit_date') # Filter options.
    search_fields = ('comment', 'user_name') # Searchable fields.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'date') # Displayed fields.
    list_filter = ('category', 'date') # Filter options.
    search_fields = ('title', 'summary', 'body') # Searchable fields.
    filter_horizontal = ('tags',) # Horizontal widget for tags.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug') # Displayed fields.
    prepopulated_fields = {'slug': ('name',)} # Auto-populate slug.

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug') # Displayed fields.
    prepopulated_fields = {'slug': ('name',)} # Auto-populate slug.

# Register models with their admin interfaces.
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)