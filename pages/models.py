from django.db import models


# Create your models here.
class AboutPage(models.Model):
    photo = models.ImageField(upload_to='about/', blank=True, null=True) # Optional image for the about page.
    body = models.TextField() # Main content of the about page.

    class Meta:
        verbose_name = "About Page" # Singular name for the admin interface.
        verbose_name_plural = "About Page" # Plural name for the admin interface.

    def __str__(self):
        return "About Page Content" # Human-readable representation.