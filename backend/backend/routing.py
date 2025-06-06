# backend/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing
import donation.routing
import notifications.routing
import help_requests.routing

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns +
            donation.routing.websocket_urlpatterns +
            notifications.routing.websocket_urlpatterns +
            help_requests.routing.websocket_urlpatterns
        )
    ),
})
