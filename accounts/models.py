from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Custom user model extending Django's built-in AbstractUser.
class CustomUser(AbstractUser):
    birthdate = models.DateField(null=True, blank=True)  # Optional birthdate field.

# User profile model with a one-to-one link to CustomUser.
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile') # Each user has one profile. Deletes profile when user is deleted.
    avatar = models.ImageField(upload_to='images/avatars', default='avatars/default.png') # Profile picture.

    def __str__(self):
        return f"{self.user.username}'s profile" # Human-readable representation.

# Signal to automatically create a Profile when a CustomUser is created.
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Signal to automatically save the Profile when its associated CustomUser is saved.
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()