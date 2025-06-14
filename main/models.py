from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

# Create your models here.
class Murders(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='murders/')
    date= models.DateTimeField(blank=True, null=True)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.name
class Suspects(models.Model):
    murders= models.ForeignKey(Murders, on_delete=models.CASCADE, related_name='suspects')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='suspects/', null=True, blank=True)
    def __str__(self):
        return self.name

class Investigators(models.Model):
    murders = models.ForeignKey(Murders, on_delete=models.CASCADE, related_name='investigations')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='investigations/', null=True, blank=True)
    def __str__(self):
        return self.name

class Interviews(models.Model):
    murders = models.ForeignKey(Murders, on_delete=models.CASCADE, related_name='interviews')
    suspects = models.ForeignKey(Suspects, on_delete=models.CASCADE, related_name='interviews')
    investigators = models.ForeignKey(Investigators, on_delete=models.CASCADE, related_name='interviews')
    content = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='interviews/', null=True, blank=True)
    def __str__(self):
        suspect_name = self.suspects.name if self.suspects else "Unknown"
        investigator_name = self.investigators.name if self.investigators else "Unknown"
        return f"Interview with {suspect_name} by {investigator_name}"




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email_verified = models.BooleanField(default=False)
    email_token = models.UUIDField(default=uuid.uuid4, editable=False)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)