from django.conf import settings


def blog_mode(request):
    return {
        'PERSONAL_BLOG_MODE': settings.PERSONAL_BLOG_MODE
    }

def social_links(request):
    social_links = getattr(settings, 'SOCIAL_LINKS', {})
    return {
        'social_links': social_links
    }