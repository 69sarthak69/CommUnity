from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notification

def create_notification(user, message, notif_type, related_object_id=None):
    notif = Notification.objects.create(
        user=user,
        message=message,
        notif_type=notif_type,
        related_object_id=related_object_id,
    )
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_{user.id}",
        {
            "type": "send_notification",
            "notification": {
                "id": str(notif.id), 
                "message": notif.message,
                "notif_type": notif.notif_type,
                "created_at": str(notif.created_at),
                "related_object_id": str(related_object_id) if related_object_id is not None else None,
            }
        }
    )
    return notif
