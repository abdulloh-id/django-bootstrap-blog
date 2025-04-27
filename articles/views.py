# Django imports
from django_comments import get_form
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
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
from django_comments.models import Comment

# Local imports
from .forms import ArticleForm, CrispyCommentForm
from .models import Article


# New Paginated Homepage View
class HomepageView(ListView):
    model = Article
    template_name = 'home.html'  # Use your homepage template
    context_object_name = 'articles'  # This will make the context variable 'articles'
    paginate_by = 5  # Number of articles per page
    ordering = ['-date']  # Order by most recent first

# View to display a list of all articles
class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'

# View to display the details of a single article
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Explicitly provide CrispyCommentForm
        context['form'] = CrispyCommentForm(target_object=self.object)
        return context

# View to update an existing article
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_edit.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

# View to delete an article
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'articles/article_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

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