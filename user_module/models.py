from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone

class User(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='user')

    def __str__(self):
        return f"{self.username} ({self.user_type})"

class Poll(models.Model):
    question = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


class Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.text} ({self.poll.question})"


class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} voted for {self.option.text}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)  
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username}"



class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contact = models.CharField(max_length=15, blank=True, default="Not Provided")
    address = models.TextField(blank=True, default="Not Provided")
    place = models.CharField(max_length=100, blank=True, default="Not Provided")
    age = models.PositiveIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True) 

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
    
        if hasattr(instance, 'userprofile'):
            instance.userprofile.save()
