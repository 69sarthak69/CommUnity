import uuid
from django.db import models
from django.conf import settings

class Notification(models.Model):
    NOTIF_TYPE_CHOICES = [
        ("application", "Application"),
        ("emergency", "Emergency"),
        ("event", "Event"),
        ("group", "Group"),
        ("post", "Post"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPE_CHOICES, default="application")  # ✅ HERE
    related_object_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.user.email} ({self.notif_type})"
