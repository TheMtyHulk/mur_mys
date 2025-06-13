from django.db import models
from main.models import Murders
# Create your models here.
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