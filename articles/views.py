from django.views.generic import (
	ListView,
	DetailView,
	UpdateView,
	DeleteView,
	CreateView,
	)
from django.urls import reverse_lazy
from .models import Article

# Define a view to display a list of all articles
class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'

# Define a view to display the details of a single article
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'

# Define a view to update an existing article
class ArticleUpdateView(UpdateView):
    model = Article
    fields = ('title', 'summary', 'body', 'photo',)
    template_name = 'article_edit.html'

# Define a view to delete an article
class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')

# Define a view to create a new article
class ArticleCreateView(CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'summary', 'body', 'photo', 'author')



