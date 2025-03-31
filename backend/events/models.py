from django.db import models
from django.conf import settings

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)

    category = models.CharField(max_length=100, default="General")  # ✅ add default
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # ✅ this one is fine as-is

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_events'
    )
    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='attending_events',
        blank=True
    )

    def attendee_count(self):
        return self.attendees.count()

    def __str__(self):
        return self.title
