# Django imports
import random
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

# Third-party imports
from django_comments import get_form
from django_comments.models import Comment

# Local imports
from .forms import ArticleForm, CrispyCommentForm
from .models import Article, Category, Tag

# Paginated homepage view for displaying articles
class HomepageView(ListView):
    model = Article
    template_name = 'home.html'  # Use your homepage template
    context_object_name = 'articles'  # This will make the context variable 'articles'
    paginate_by = 10  # Number of articles per page
    ordering = ['-date']  # Order by most recent first

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

# Mixin for sidebar context
class SidebarContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Categories with article counts (optimized)
        categories_with_count = Category.objects.annotate(count=Count('articles')).all()
        context['categories_with_count'] = [
            {'category': category, 'count': category.count}
            for category in categories_with_count
        ]

        # Random tags (up to 10)
        all_tags = Tag.objects.all()
        context['random_tags'] = random.sample(list(all_tags), min(10, len(all_tags)))

        # Latest 5 articles
        latest_articles = Article.objects.order_by('-date')[:5]
        context['latest_articles'] = latest_articles

        return context

class ArticleListView(SidebarContextMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'object_list'
    paginate_by = 10
    ordering = ['-date']

class CategoryArticleListView(SidebarContextMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'object_list'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Article.objects.filter(category=self.category).order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.category
        return context

class TagArticleListView(SidebarContextMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'object_list'
    paginate_by = 10

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Article.objects.filter(tags=self.tag).order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_tag'] = self.tag
        return context

class SearchArticleView(SidebarContextMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'object_list'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Article.objects.filter(
                Q(title__icontains=query) | 
                Q(summary__icontains=query) | 
                Q(body__icontains=query)
            ).order_by('-date')
        return Article.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

# View to create a new article
class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_new.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

# View to update an existing article
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_edit.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

# View to display the details of a single article
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Explicitly provide CrispyCommentForm
        context['form'] = CrispyCommentForm(target_object=self.object)
        context['categories'] = Category.objects.all()
        return context

# View to delete an article
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'articles/article_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

# View to delete comments by staff members
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_id'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_success_url(self):
        article = self.object.content_object
        return article.get_absolute_url()
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Izoh muvaffaqiyatli o'chirildi.")
        return redirect(success_url)
    
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
