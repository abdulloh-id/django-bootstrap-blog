from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleUpdateView,
    ArticleDeleteView,
    ArticleCreateView,
)

# Class-based views
urlpatterns = [
    path('<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),  # Edit an existing article
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),  # View details of an article
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),  # Delete an article
    path('new/', ArticleCreateView.as_view(), name='article_new'),  # Create a new article
    path('', ArticleListView.as_view(), name='article_list'),  # List all articles
]