from django.db import migrations
from django.utils.text import slugify

def create_default_categories(apps, schema_editor):
    Category = apps.get_model('articles', 'Category')
    
    # Define your initial categories here
    categories = ['Lifestyle', 'Tourism', 'Gastronomy', 'Psychology', 'General']
    
    for name in categories:
        Category.objects.get_or_create(
            name=name,
            slug=slugify(name) # This turns "Web Development" into "web-development"
        )

class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'), # Make sure this matches your first migration name
    ]

    operations = [
        migrations.RunPython(create_default_categories),
    ]