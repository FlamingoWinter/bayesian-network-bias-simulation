from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path

from backend.api.api.consumers import generate_random_network_consumer
from backend.api.api.consumers import name_network_consumer
from backend.api.api.consumers import simulate_consumer

websocket_urlpatterns = [
    re_path(r'ws/generate-random-network', generate_random_network_consumer.GenerateRandomNetworkConsumer.as_asgi()),
    re_path(r'ws/name-network', name_network_consumer.NameNetworkConsumer.as_asgi()),
    re_path(r'ws/simulate', simulate_consumer.SimulateConsumer.as_asgi()),

]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
