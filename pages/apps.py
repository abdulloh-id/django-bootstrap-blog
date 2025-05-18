from django.apps import AppConfig


class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' # Use BigAutoField for primary keys by default.
    name = 'pages' # Unique name of this application.