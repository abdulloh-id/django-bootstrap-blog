import environ
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    
    def ready(self):
        """This runs when Django starts up"""
        import time
        time.sleep(2)  # Give database time to be ready
        
        # Create superuser if needed
        self.create_superuser_if_needed()
        
        # Update site information
        self.update_site_info()
    
    def create_superuser_if_needed(self):
        """Create a superuser if none exists"""
        try:
            env = environ.Env()
            from accounts.models import CustomUser
            
            if not CustomUser.objects.filter(is_superuser=True).exists():
                CustomUser.objects.create_superuser(
                    username=env('DJANGO_SUPERUSER_USERNAME', default='admin'),
                    email=env('DJANGO_SUPERUSER_EMAIL', default='admin@example.com'),
                    password=env('DJANGO_SUPERUSER_PASSWORD', default='123456')
                )
                print("Superuser created successfully!")
        except Exception as e:
            # Database might not be ready yet during migrations, that's okay
            print(f"Couldn't create superuser: {e}")
    
    def update_site_info(self):
        """Update Django site information from environment variables"""
        try:
            import environ
            from django.contrib.sites.models import Site
            
            env = environ.Env()
            site, created = Site.objects.get_or_create(
                pk=1,
                defaults={
                    'name': env('SITE_NAME', default='My Blog'),
                    'domain': env('SITE_DOMAIN', default='localhost:8000')
                }
            )
            if not created:
                site.name = env('SITE_NAME', default='My Blog')
                site.domain = env('SITE_DOMAIN', default='localhost:8000')
                site.save()
                print(f"Site info updated: {site.name} - {site.domain}")
        except Exception as e:
            print(f"Couldn't update site info: {e}")
            pass  # Ignore errors during container startup