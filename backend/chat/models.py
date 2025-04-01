from django.db import models
from django.conf import settings

class Room(models.Model):
    """One room per group or event"""
    name = models.CharField(max_length=100, unique=True)  # ex: "group_5"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    """Messages inside a room"""
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} @ {self.room.name}: {self.content[:30]}"
