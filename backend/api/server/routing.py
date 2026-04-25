from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path

from backend.api.websocket_consumers import generate_network
from backend.api.websocket_consumers import name_network
from backend.api.websocket_consumers import simulate

websocket_urlpatterns = [
    re_path(
        r"ws/generate-random-network",
        generate_network.GenerateRandomNetworkConsumer.as_asgi(),  # type: ignore
    ),
    re_path(r"ws/name-network", name_network.NameNetworkConsumer.as_asgi()),  # type: ignore
    re_path(r"ws/simulate", simulate.SimulateConsumer.as_asgi()),  # type: ignore
]

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
