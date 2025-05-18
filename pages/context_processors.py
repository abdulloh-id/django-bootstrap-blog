def social_links(request):
    """
    Make social media links available to all templates.
    """
    from django.conf import settings

    # Get social links from settings with empty defaults
    # This ensures the template won't break if a link is missing
    social_links = getattr(settings, 'SOCIAL_LINKS', {})
    
    return {
        'social_links': social_links
    }