from django.apps import AppConfig


# Configuration for the 'accounts' application.
class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Use BigAutoField as the default primary key type.
    name = 'accounts'  # The unique name of this application.