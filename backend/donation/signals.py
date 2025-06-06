# donation/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DonationCampaign
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import DonationCampaignSerializer

@receiver(post_save, sender=DonationCampaign)
def broadcast_donation_campaign_update(sender, instance, created, **kwargs):
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync

    channel_layer = get_channel_layer()

    # Remove status check — just notify on save
    async_to_sync(channel_layer.group_send)(
        "donations",
        {
            "type": "donation_update",
            "data": {
                "message": "Donation campaign updated",
                "campaign_id": instance.id,
            },
        }
    )

