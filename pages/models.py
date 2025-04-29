from django.db import models

# Create your models here.
class AboutPage(models.Model):
    photo = models.ImageField(upload_to='about/', blank=True, null=True)
    body = models.TextField()
    
    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"
    
    def __str__(self):
        return "About Page Content"
