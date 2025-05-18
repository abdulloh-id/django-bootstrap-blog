from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100) # Category name.
    slug = models.SlugField(unique=True) # URL-friendly version.

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories' # Human-readable plural name.

class Tag(models.Model):
    name = models.CharField(max_length=50) # Tag name.
    slug = models.SlugField(unique=True) # URL-friendly version.

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=150) # Article title.
    summary = models.CharField(max_length=250, blank=True) # Short description.
    body = models.TextField() # Main content.
    photo = models.ImageField(upload_to='images/', blank=True) # Optional image.
    date = models.DateTimeField(auto_now_add=True) # Creation timestamp.
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE) # Author of the article.
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles') # Article category.
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles') # Keywords for the article.

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)]) # URL to view this article.