"""
Tests for api/server/apps.py.

When the server starts, all predefined networks should be loaded into the cache
so that pages relying on them (e.g. the default network view) are fast on first
load.  This test verifies that the startup routine caches each named network.
"""

import importlib
import sys
import pytest
from unittest.mock import patch


def make_config():
    """
    Return a fresh ServerConfig instance without going through Django's
    app-registry machinery (which would fail outside a real server process).
    """
    from backend.api.server.apps import ServerConfig
    app_module = importlib.import_module("backend.api.server")
    return ServerConfig("server", app_module)


def test_startup_loads_all_predefined_networks_into_cache():
    """
    ServerConfig.ready() should cache the sprinkler, shark sighting,
    random seeded, and named seeded networks under their respective keys.
    """
    with patch(
        "backend.api.server.apps.cache_network_and_generate_applicants"
    ) as mock_cache, patch.object(sys, "argv", ["runserver"]):
        config = make_config()
        config.ready()

    # Extract session_id args (second positional arg) from all calls
    cached_keys = {
        c.args[1] for c in mock_cache.call_args_list if len(c.args) > 1
    }

    assert "sprinkler" in cached_keys
    assert "shark_sighting" in cached_keys
    assert "random_seeded" in cached_keys
    assert "named_seeded" in cached_keys


def test_startup_also_caches_a_default_network():
    """
    One network should also be cached under the default key so that the
    landing page works before a user has generated their own.
    """
    with patch(
        "backend.api.server.apps.cache_network_and_generate_applicants"
    ) as mock_cache, patch.object(sys, "argv", ["runserver"]):
        config = make_config()
        config.ready()

    # At least one call should have no session_id (default network)
    calls_with_no_key = [c for c in mock_cache.call_args_list if len(c.args) == 1]
    assert len(calls_with_no_key) >= 1


def test_startup_is_skipped_during_migrations():
    """
    Running migrations should not trigger network generation — that would
    be slow and unnecessary during database setup.
    """
    with patch(
        "backend.api.server.apps.cache_network_and_generate_applicants"
    ) as mock_cache, patch.object(sys, "argv", ["manage.py", "migrate"]):
        config = make_config()
        config.ready()

    mock_cache.assert_not_called()
