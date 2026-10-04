"""
Tests for api/server/routing.py.

The frontend opens three WebSocket connections, one for each step of the
workflow.  The routing table must map every route the frontend uses to a
consumer, and every consumer must be reachable via some route.
"""

import re
import pytest

# Routes that the frontend actually connects to (from src/stores/functions.ts)
FRONTEND_WEBSOCKET_ROUTES = [
    "ws/generate-random-network",
    "ws/name-network",
    "ws/simulate",
]


@pytest.fixture(scope="module")
def websocket_patterns():
    from backend.api.server.routing import websocket_urlpatterns
    return websocket_urlpatterns


def test_every_frontend_route_is_handled(websocket_patterns):
    """
    Every WebSocket path the frontend opens must have a matching entry in the
    routing table.  A missing route would cause the frontend to hang silently.
    """
    raw_patterns = [p.pattern.regex.pattern for p in websocket_patterns]
    for route in FRONTEND_WEBSOCKET_ROUTES:
        matched = any(re.search(re.escape(route), p) for p in raw_patterns)
        assert matched, (
            f"Frontend route '{route}' has no matching entry in websocket_urlpatterns"
        )


def test_every_routed_consumer_is_a_websocket_consumer(websocket_patterns):
    """
    Every entry in the routing table should point to a real WebSocket consumer,
    not a placeholder or mis-imported object.
    """
    from channels.generic.websocket import AsyncWebsocketConsumer

    for pattern in websocket_patterns:
        consumer_cls = pattern.callback.cls
        assert issubclass(consumer_cls, AsyncWebsocketConsumer), (
            f"Pattern '{pattern.pattern}' does not point to an AsyncWebsocketConsumer"
        )


def test_no_two_routes_point_to_the_same_consumer(websocket_patterns):
    """
    Each consumer should own exactly one route.  Sharing a route would mean
    one consumer is unreachable.
    """
    consumer_classes = [p.callback.cls for p in websocket_patterns]
    assert len(consumer_classes) == len(set(consumer_classes)), (
        "Two or more routes point to the same consumer class"
    )
