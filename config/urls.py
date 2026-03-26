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
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


def comment_redirect(request):
    """ Redirect users back to the article instead of showing 'Thank You' """
    return redirect(request.GET.get('next', '/'))

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. THE BIG CHANGE: Move articles to the root
    path('', include('articles.urls')), 
    
    # 2. Authentication & Accounts
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    
    # 3. Comments System
    path('comments/', include('django_comments.urls')),
    path('comments/posted/', comment_redirect, name='comments-comment-done'),
    
    # 4. Other static pages (About, Contact, etc.)
    path('pages/', include('pages.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)