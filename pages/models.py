from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class AboutPage(models.Model):
    photo = models.ImageField(upload_to='about/', blank=True, null=True) # Optional image for the about page.
    body = models.TextField() # Main content of the about page.

    class Meta:
        verbose_name = "About Page" # Singular name for the admin interface.
        verbose_name_plural = "About Page" # Plural name for the admin interface.

    def __str__(self):
        return "About Page Content" # Human-readable representation.

class ContactMessage(models.Model):
    name = models.CharField(_("Your Name"), max_length=100)
    email = models.EmailField(_("Your Email"))
    message = models.TextField(_("Your Message"))
    created_at = models.DateTimeField(_("Sent At"), auto_now_add=True)
    is_processed = models.BooleanField(_("Processed / Replied"), default=False)

    class Meta:
        verbose_name = _("Contact Message")
        verbose_name_plural = _("Contact Messages")
        ordering = ['-created_at']

    def __summary__(self):
        return f"Message from {self.name} ({self.email})"