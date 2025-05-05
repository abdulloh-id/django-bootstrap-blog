from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleUpdateView,
    ArticleDeleteView,
    ArticleCreateView,
    CommentDeleteView,
    HomepageView,
    CategoryArticleListView,
    TagArticleListView,
)

# Class-based views
urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('new/', ArticleCreateView.as_view(), name='article_new'),
    path('comments/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
    
    # New URLs for category and tag filtering
    path('category/<slug:slug>/', CategoryArticleListView.as_view(), name='category_articles'),
    path('tag/<slug:slug>/', TagArticleListView.as_view(), name='tag_articles'),
]