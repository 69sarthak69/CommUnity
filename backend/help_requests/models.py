import uuid
from django.db import models
from django.conf import settings

class HelpRequest(models.Model):
    """Model for user help requests"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    applicants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='applied_requests', blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    CATEGORY_CHOICES = [
        ("food", "Food"),
        ("medical", "Medical Aid"),
        ("education", "Education"),
        ("emergency", "Emergency"),
        ("other", "Other"),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    location = models.CharField(max_length=100)  # Stores city names only

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("completed", "Completed"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    is_emergency = models.BooleanField(default=False)  # Emergency mode flag
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

class HelpResponse(models.Model):
    """Model for users offering help"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request = models.ForeignKey(HelpRequest, on_delete=models.CASCADE, related_name="responses")
    helper = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="help_responses")
    message = models.TextField(blank=True, null=True)

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("completed", "Completed"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to {self.request.title} by {self.helper}"
    


# Add to models.py
class CommunityPost(models.Model):
    """Model for general community posts"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="community_posts")
    title = models.CharField(max_length=255)
    content = models.TextField()
    
    CATEGORY_CHOICES = [
        ("general", "General"),
        ("event", "Event"),
        ("alert", "Alert"),
        ("lost_found", "Lost & Found"),
        ("recommendation", "Recommendation"),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="general")

    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.email})"
    

class HelpApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    help_request = models.ForeignKey(HelpRequest, on_delete=models.CASCADE, related_name="applications")
    letter = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'help_request')

    def __str__(self):
        return f"{self.user.email} applied to {self.help_request.title}"


class Comment(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
