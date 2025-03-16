from django.urls import path, include
from .views import (
	ArticleListView,
	ArticleUpdateView,
	ArticleDetailView,
	ArticleDeleteView,
	ArticleCreateView,
	)
from django.shortcuts import redirect


def comment_redirect(request):
    """ Redirect users back to the article instead of showing 'Thank You' """
    return redirect(request.GET.get('next', '/'))

urlpatterns = [
	path('<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
	path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
	path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
	path('new/', ArticleCreateView.as_view(), name='article_new'),
	path('', ArticleListView.as_view(), name='article_list'),
	path('comments/', include('django_comments.urls')),
	path('comments/posted/', comment_redirect, name='comments-comment-done'),  # Override default
]

