from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    roomId = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=10, default='DM')
    members = models.ManyToManyField(User, related_name='chat_rooms')
    name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.roomId


class ChatMessage(models.Model):
    chat = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}"
