from django.apps import AppConfig
import environ


# Configuration for the 'accounts' application.
class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Use BigAutoField as the default primary key type.
    name = 'accounts'  # The unique name of this application.
    z
    def ready(self):
        # This runs when Django starts up
        self.create_superuser_if_needed()
    
    def create_superuser_if_needed(self):
        try:
            # Initialize environ
            env = environ.Env()
            
            from accounts.models import CustomUser
            
            if not CustomUser.objects.filter(is_superuser=True).exists():
                CustomUser.objects.create_superuser(
                    username=env('DJANGO_SUPERUSER_USERNAME', default='admin'),
                    email=env('DJANGO_SUPERUSER_EMAIL', default='admin@example.com'),
                    password=env('DJANGO_SUPERUSER_PASSWORD', default='defaultpass123')
                )
                print("Superuser created successfully!")
        except Exception as e:
            # Database might not be ready yet during migrations, that's okay
            print(f"Couldn't create superuser: {e}")