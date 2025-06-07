from django.db import models

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



class ChatRoom(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    murder_case = models.ForeignKey(Murders, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Chat: {self.subject} - {self.user.username}"
    
    class Meta:
        ordering = ['-updated_at']

class ChatMessage(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.TextField()
    is_admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.sender.username}: {self.message[:50]}..."
    
    class Meta:
        ordering = ['timestamp']