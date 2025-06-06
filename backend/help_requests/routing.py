from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/notifications/(?P<user_id>\d+)/$", consumers.NotificationConsumer.as_asgi()),
    re_path(r"ws/help-request/(?P<help_request_id>\w+)/$", consumers.HelpRequestConsumer.as_asgi()),

    re_path(r"ws/feed/$", consumers.CommunityFeedConsumer.as_asgi()),
    
]
