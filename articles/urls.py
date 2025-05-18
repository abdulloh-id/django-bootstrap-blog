from django.urls import path

from .views import (ArticleCreateView, ArticleDeleteView, ArticleDetailView,
                    ArticleListView, ArticleUpdateView,
                    CategoryArticleListView, CommentDeleteView, HomepageView,
                    SearchArticleView, TagArticleListView)

# URL patterns for class-based views.
urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'), # List all articles.
    path('<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'), # Edit an existing article.
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'), # View a single article.
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'), # Delete an article.
    path('new/', ArticleCreateView.as_view(), name='article_new'), # Create a new article.
    path('comments/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='delete_comment'), # Delete a comment.

    # URLs for filtering articles by category and tag.
    path('category/<slug:slug>/', CategoryArticleListView.as_view(), name='category_articles'), # Articles in a specific category.
    path('tag/<slug:slug>/', TagArticleListView.as_view(), name='tag_articles'), # Articles with a specific tag.

    # URL for searching articles.
    path('search/', SearchArticleView.as_view(), name='article_search'), # Search articles.
]