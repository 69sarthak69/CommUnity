from .models import Notification

def create_notification(user, message, notif_type, related_object_id=None):
    Notification.objects.create(
        user=user,
        message=message,
        notif_type=notif_type,
        related_object_id=related_object_id
    )
