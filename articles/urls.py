from django.urls import path
from .views import (
    ArticleCreateView, ArticleDeleteView, ArticleDetailView,
    ArticleListView, ArticleUpdateView, CategoryArticleListView, 
    CommentDeleteView, SearchArticleView, TagArticleListView
)

urlpatterns = [
    # 1. Global / Navigation Paths
    path('', ArticleListView.as_view(), name='home'),
    path('search/', SearchArticleView.as_view(), name='article_search'),
    path('category/<slug:slug>/', CategoryArticleListView.as_view(), name='category_articles'),
    path('tag/<slug:slug>/', TagArticleListView.as_view(), name='tag_articles'),

    # 2. CRUD Paths (Create, Read, Update, Delete)
    path('new/', ArticleCreateView.as_view(), name='article_new'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),

    # 3. Specialized Paths
    path('comments/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
]