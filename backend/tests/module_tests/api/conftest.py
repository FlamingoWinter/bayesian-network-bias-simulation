"""
Shared setup for API module tests.

Adds backend/api to sys.path so that Django can find the `server` package,
and provides a fixture that pre-populates the Django cache with a small seeded
network so consumer and view tests don't need to generate one themselves.
"""

import sys
import os
import pytest

# Make `server` importable (it lives at backend/api/server/)
_api_dir = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "api")
)
if _api_dir not in sys.path:
    sys.path.insert(0, _api_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")


@pytest.fixture()
def cached_network():
    """
    Stores a small seeded network in the Django cache under both the
    default key (used by views) and a test session key, then returns
    the session key and network for use in tests.

    Uses LocMemCache (configured in test_settings), so no database is needed.
    """
    from backend.simulation.build_network.generation.generate_categorical_network import (
        generate_random_categorical_network,
    )
    from backend.api.cache import cache_network_and_generate_applicants

    network = generate_random_categorical_network(nodes=15, seed=42)
    session_key = "test-session"
    cache_network_and_generate_applicants(network, session_key)
    cache_network_and_generate_applicants(network)  # default key for views
    return session_key, network
