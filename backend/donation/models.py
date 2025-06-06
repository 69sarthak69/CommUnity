# donation/models.py
from django.db import models
from django.conf import settings
from help_requests.models import HelpRequest
from groups.models import Group

class DonationCampaign(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    location = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    help_request = models.ForeignKey(HelpRequest, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

class Donation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    campaign = models.ForeignKey(DonationCampaign, on_delete=models.CASCADE, null=True, blank=True)  # Made nullable
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    pidx = models.CharField(max_length=100, null=True, blank=True)
    anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.anonymous:
            return f"Anonymous donated Rs. {self.amount} to {self.campaign or 'No Campaign'}"
        return f"{self.user} donated Rs. {self.amount} to {self.campaign or 'No Campaign'}"

class InKindDonation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    drop_off_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='in_kind_donations/', null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item} by {self.user or 'Anonymous'}"