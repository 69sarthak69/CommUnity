import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

from chat.routing import websocket_urlpatterns as chat_ws
from donation.routing import websocket_urlpatterns as donation_ws
from notifications.routing import websocket_urlpatterns as notifications_ws
from help_requests.routing import websocket_urlpatterns as help_requests_ws

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat_ws + donation_ws + notifications_ws + help_requests_ws 
        )
    ),
})
