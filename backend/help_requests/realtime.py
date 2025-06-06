# help_requests/realtime.py
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .serializers import HelpRequestSerializer
from .serializers import CommunityPostSerializer

def broadcast_new_help_request(help_request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "community_feed",  # group name
        {
            "type": "send_feed_update",
            "data": {
                "type": "new_help_request",
                **HelpRequestSerializer(help_request).data
            }
        }
    )


def broadcast_new_community_post(post):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "community_feed",
        {
            "type": "send_feed_update",
            "data": {
                "type": "new_community_post",
                **CommunityPostSerializer(post).data
            }
        }
    )