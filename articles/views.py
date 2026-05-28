import os
import random

import environ
from django.conf import settings

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)
from django_comments import get_form
from django_comments.models import Comment

from .forms import ArticleForm, CrispyCommentForm
from .models import Article, Category, Tag

# Initialize environ once at module level
env = environ.Env()
environ.Env.read_env()

@csrf_exempt
def tinymce_upload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        img = request.FILES['file']
        # Define where to save
        path = os.path.join(settings.MEDIA_ROOT, 'tinymce', img.name)
        
        # Save file to disk
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb+') as destination:
            for chunk in img.chunks():
                destination.write(chunk)
        
        # Return the URL for TinyMCE to insert into the HTML
        return JsonResponse({'location': f"{settings.MEDIA_URL}tinymce/{img.name}"})
    return JsonResponse({'error': 'Failed to upload'}, status=400)

class SidebarContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['categories_with_count'] = Category.objects.annotate(
            article_count=Count('articles')
        ).order_by('-article_count')

        context['random_tags'] = Tag.objects.order_by('?')[:10]

        context['latest_articles'] = Article.objects.order_by('-date')[:5]
        return context

class ArticleListView(SidebarContextMixin, ListView):
    model = Article
    template_name = 'articles/list.html' # Fixed path
    context_object_name = 'object_list'
    paginate_by = env.int('ITEMS_PER_PAGE', default=10)
    ordering = ['-date']

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
        context['current_category'] = self.category
        return context

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
        context['current_tag'] = self.tag
        return context

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
        return Article.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/update.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ArticleDetailView(SidebarContextMixin, DetailView):
    model = Article
    template_name = 'articles/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CrispyCommentForm(target_object=self.object)
        return context

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'articles/delete.html'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

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
        messages.success(request, _("Comment deleted successfully."))
        return redirect(success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)