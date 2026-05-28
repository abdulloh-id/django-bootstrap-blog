"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


def comment_redirect(request):
    """ Redirect users back to the article instead of showing 'Thank You' """
    return redirect(request.GET.get('next', '/'))

# Global paths that shouldn't have language prefixes (like language switchers or API endpoints)
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('articles.urls')), 
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('comments/', include('django_comments.urls')),
    path('comments/posted/', comment_redirect, name='comments-comment-done'),
    path('pages/', include('pages.urls')), 
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)