from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView,
    TemplateView,  # Add this import
)
from django.urls import reverse_lazy
from .models import Article
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ArticleForm
from .forms import CrispyCommentForm

# New Paginated Homepage View
class HomepageView(ListView):
    model = Article
    template_name = 'index-full.html'  # Use your homepage template
    context_object_name = 'articles'  # This will make the context variable 'articles'
    paginate_by = 5  # Number of articles per page
    ordering = ['-date']  # Order by most recent first

# Keep your existing views, just add the HomepageView above
class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'

# View to display a list of all articles
class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'

# View to display the details of a single article
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'

# View to update an existing article
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_edit.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

# View to delete an article
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('index-full')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

# View to create a new article
class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_new.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser