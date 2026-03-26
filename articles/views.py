# Standard imports
import random

import environ
# Django and third-party imports
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)
from django_comments import get_form
from django_comments.models import Comment

# Local imports
from .forms import ArticleForm, CrispyCommentForm
from .models import Article, Category, Tag

# Initialize environ once at module level
env = environ.Env()
environ.Env.read_env()  # This reads the .env file

# Mixin to add sidebar context data.
class SidebarContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Efficient annotation
        context['categories_with_count'] = Category.objects.annotate(
            article_count=Count('articles')
        ).order_by('-article_count')

        # Database-level random selection (Much faster)
        context['random_tags'] = Tag.objects.order_by('?')[:10]

        # Latest articles
        context['latest_articles'] = Article.objects.order_by('-date')[:5]
        return context

# View to list all articles with pagination and sidebar.
class ArticleListView(SidebarContextMixin, ListView):
    model = Article
    template_name = 'articles/list.html' # Fixed path
    context_object_name = 'object_list'
    paginate_by = env.int('ITEMS_PER_PAGE', default=10)
    ordering = ['-date']

# View to list articles belonging to a specific category.
class CategoryArticleListView(SidebarContextMixin, ListView):
    model = Article
    template_name = 'articles/list.html'
    context_object_name = 'object_list'
    paginate_by = env.int('ITEMS_PER_PAGE', default=10)

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Article.objects.filter(category=self.category).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.category  # Current category for template.
        return context

# View to list articles tagged with a specific tag.
class TagArticleListView(SidebarContextMixin, ListView):
    model = Article
    template_name = 'articles/list.html'
    context_object_name = 'object_list'
    paginate_by = env.int('ITEMS_PER_PAGE', default=10)

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Article.objects.filter(tags=self.tag).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_tag'] = self.tag  # Current tag for template.
        return context

# View to search articles based on a query.
class SearchArticleView(SidebarContextMixin, ListView):
    model = Article
    template_name = 'articles/list.html'
    context_object_name = 'object_list'
    paginate_by = env.int('ITEMS_PER_PAGE', default=10)

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Article.objects.filter(
                Q(title__icontains=query) |
                Q(summary__icontains=query) |
                Q(body__icontains=query)
            ).order_by('-date')
        return Article.objects.none()  # Return empty queryset if no query.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')  # Search query for template.
        return context

# View to create a new article (requires login and staff status).
class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set author to logged-in user.
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff  # Only staff can create articles.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # All categories for form.
        return context

# View to update an existing article (requires login and ownership).
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/update.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user  # Only author can edit.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # All categories for form.
        return context

# View to display the details of a single article and its comments.
class ArticleDetailView(SidebarContextMixin, DetailView):
    model = Article
    template_name = 'articles/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CrispyCommentForm(target_object=self.object)
        # No need to manually add categories here anymore, the Mixin does it!
        return context

# View to delete an article (requires login and ownership).
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'articles/delete.html'
    success_url = reverse_lazy('home')  # Redirect after deletion.
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user  # Only author can delete.

# View to delete comments (requires login and staff status).
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_id'  # URL parameter for comment ID.

    def test_func(self):
        return self.request.user.is_staff  # Only staff can delete comments.

    def get_success_url(self):
        article = self.object.content_object  # Get the associated article.
        return article.get_absolute_url()  # Redirect to article detail.

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Izoh muvaffaqiyatli o'chirildi.")  # Success message.
        return redirect(success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)  # Allow deletion via GET.