"""
Tests for api/websocket_consumers/.

Each WebSocket consumer handles one step of the user's workflow.  A client
opens a connection, sends a JSON message describing what it wants, receives
progress updates, and then the connection closes.

These tests verify that each consumer:
  - accepts the connection
  - does the work it claims to do (network in cache, bias in cache, etc.)
  - sends the right completion messages

All tests are written as synchronous functions using asgiref's async_to_sync
wrapper so they work reliably with pytest-django's database fixtures.
"""

import json
import pytest
from asgiref.sync import async_to_sync
from channels.testing import WebsocketCommunicator


# ── Helpers ───────────────────────────────────────────────────────────────────


async def _collect_messages(communicator, timeout=10):
    """Drain all messages until the socket closes or times out."""
    messages = []
    while True:
        try:
            msg = await communicator.receive_from(timeout=timeout)
            messages.append(json.loads(msg))
        except Exception:
            break
    return messages


# ── generate_network consumer ─────────────────────────────────────────────────


@pytest.mark.django_db(transaction=True)
def test_generate_random_network_caches_a_network_and_confirms_completion():
    """
    When a client requests a random network, the consumer should generate one,
    store it in the cache under the client's session key, and confirm that both
    the network and the applicant pool are ready.
    """
    from backend.api.server.routing import application
    from backend.api.cache import get_network_from_cache

    session_key = "test-random-gen"

    async def _run():
        communicator = WebsocketCommunicator(
            application, f"/ws/generate-random-network/?session_key={session_key}"
        )
        connected, _ = await communicator.connect()
        assert connected

        await communicator.send_json_to({
            "random_or_predefined": "random",
            "number_of_nodes": 15,
            "parents_range": [1, 2],
            "mutual_information_range": [0.4, 0.8],
            "values_per_variable": {"2": 0.7, "3": 0.3},
        })

        messages = await _collect_messages(communicator)
        return [m["message"] for m in messages]

    text = async_to_sync(_run)()
    assert "Network Generation Completed" in text
    assert "Candidate Generation Completed" in text

    network = get_network_from_cache(session_key)
    assert network is not None
    assert len(network.characteristics) == 15


@pytest.mark.django_db(transaction=True)
def test_generate_predefined_network_loads_sprinkler_and_confirms_completion():
    """
    When a client requests the sprinkler predefined network, the consumer should
    load it and confirm it is ready — without running any generation.
    """
    from backend.api.server.routing import application
    from backend.api.cache import get_network_from_cache

    session_key = "test-predefined-sprinkler"

    async def _run():
        communicator = WebsocketCommunicator(
            application, f"/ws/generate-random-network/?session_key={session_key}"
        )
        connected, _ = await communicator.connect()
        assert connected

        await communicator.send_json_to({
            "random_or_predefined": "predefined",
            "predefined_model": "sprinkler",
        })

        messages = await _collect_messages(communicator)
        return [m["message"] for m in messages]

    text = async_to_sync(_run)()
    assert "Network Generation Completed" in text
    assert "Candidate Generation Completed" in text

    network = get_network_from_cache(session_key)
    assert network is not None


@pytest.mark.django_db(transaction=True)
def test_generate_network_sends_error_for_unknown_predefined_model():
    """
    If the client requests a predefined model that doesn't exist, the consumer
    should send an error message instead of crashing.
    """
    from backend.api.server.routing import application

    async def _run():
        communicator = WebsocketCommunicator(
            application,
            "/ws/generate-random-network/?session_key=test-bad-predefined",
        )
        connected, _ = await communicator.connect()
        assert connected

        await communicator.send_json_to({
            "random_or_predefined": "predefined",
            "predefined_model": "does_not_exist",
        })

        return await _collect_messages(communicator)

    messages = async_to_sync(_run)()
    assert any(m.get("error") for m in messages)


# ── name_network consumer ─────────────────────────────────────────────────────


@pytest.mark.django_db(transaction=True)
def test_name_network_gives_all_characteristics_meaningful_english_names(
    cached_network,
):
    """
    After naming, no characteristic should still have a raw numeric name like
    '0' or '7'.  All nodes should carry names drawn from the domain vocabulary.
    """
    from backend.api.server.routing import application
    from backend.api.cache import get_network_from_cache

    session_key, _ = cached_network

    async def _run():
        communicator = WebsocketCommunicator(
            application, f"/ws/name-network/?session_key={session_key}"
        )
        connected, _ = await communicator.connect()
        assert connected

        await communicator.send_to(text_data="{}")
        messages = await _collect_messages(communicator)
        return [m["message"] for m in messages]

    text = async_to_sync(_run)()
    assert "Network Renaming Completed" in text
    assert "Candidate Generation Completed" in text

    renamed = get_network_from_cache(session_key)
    for name in renamed.characteristics:
        assert not name.isdigit(), (
            f"Characteristic '{name}' still has a numeric name after renaming"
        )


# ── simulate consumer ─────────────────────────────────────────────────────────


@pytest.mark.django_db(transaction=True)
def test_simulate_stores_bias_results_in_cache_for_all_requested_recruiters(
    cached_network,
):
    """
    After a simulation run, bias results for every requested recruiter should
    be stored in the cache so that subsequent HTTP requests can retrieve them.
    """
    from backend.api.server.routing import application
    from backend.api.cache import from_cache

    session_key, network = cached_network
    protected = list(network.characteristics.keys())[0]

    async def _run():
        communicator = WebsocketCommunicator(
            application, f"/ws/simulate/?session_key={session_key}"
        )
        connected, _ = await communicator.connect()
        assert connected

        await communicator.send_json_to({
            "candidates_to_generate": 200,
            "recruiters": {"logistic_regression": ["no_mitigation"]},
            "protected_characteristic": protected,
            "score_threshold": 0,
        })

        await _collect_messages(communicator)

    async_to_sync(_run)()

    bias = from_cache(f"bias_{session_key}")
    assert bias is not None
    assert "Logistic Regression" in bias
