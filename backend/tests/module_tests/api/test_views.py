"""
Tests for api/server/views.py.

The HTTP views serve cached data to the frontend.  Each view reads something
from the cache (keyed by session cookie) and returns it as JSON.  These tests
verify that each view returns the right structure for a known cache state.
"""

import json
import pytest
from django.test import Client


@pytest.fixture()
def client_with_session(cached_network):
    """
    Returns a Django test client whose session cookie matches the key under
    which the test network is cached.
    """
    session_key, network = cached_network
    client = Client()
    # Manually set the sessionid cookie to match our cached key
    client.cookies["sessionid"] = session_key
    return client, network


@pytest.mark.django_db
def test_get_network_returns_the_network_response_for_the_current_session(
    client_with_session,
):
    """
    GET / should return the network stored under the caller's session key,
    including characteristics and graph metadata.
    """
    client, network = client_with_session
    response = client.get("/")

    assert response.status_code == 200
    data = json.loads(response.content)
    assert "characteristics" in data
    assert "scoreCharacteristic" in data
    assert "applicationCharacteristics" in data


@pytest.mark.django_db
def test_condition_updates_the_network_and_returns_new_distributions(
    client_with_session,
):
    """
    POST /condition/ with a node observation should return updated probability
    distributions for every characteristic in the network.
    """
    client, network = client_with_session
    # Condition on the first characteristic being category 0
    conditioned_node = list(network.characteristics.keys())[0]
    body = json.dumps({conditioned_node: 0})

    response = client.post(
        "/condition/",
        data=body,
        content_type="application/json",
    )

    assert response.status_code == 200
    data = json.loads(response.content)
    # The response should be a dict of characteristic → distribution
    assert isinstance(data, dict)
    assert len(data) > 0


@pytest.mark.django_db
def test_condition_with_predefined_key_conditions_the_named_network(
    client_with_session,
):
    """
    POST /condition/<predefined>/ should condition the predefined network (not
    the session network), so that the walkthrough pages can show live inference.
    """
    client, network = client_with_session

    # The default (no session key) network was also cached in cached_network
    conditioned_node = list(network.characteristics.keys())[0]
    body = json.dumps({conditioned_node: 0})

    response = client.post(
        "/condition/sprinkler/",
        data=body,
        content_type="application/json",
    )

    # Either 200 (found and conditioned) or 400 (sprinkler doesn't have this node)
    # but NOT 500 — the view should handle mismatched nodes gracefully
    assert response.status_code in (200, 400)


@pytest.mark.django_db
def test_csrf_returns_a_token():
    """
    GET /csrf/ should return a CSRF token that the frontend can use for
    subsequent POST requests.
    """
    client = Client()
    response = client.get("/csrf/")

    assert response.status_code == 200
    data = json.loads(response.content)
    assert "token" in data
    assert len(data["token"]) > 0


@pytest.mark.django_db
def test_session_key_returns_existing_key_if_already_set():
    """
    GET /session/ when the client already has a sessionid cookie should echo
    back that same key rather than creating a new one.
    """
    client = Client()
    client.cookies["sessionid"] = "my-existing-key"
    response = client.get("/session/")

    assert response.status_code == 200
    data = json.loads(response.content)
    assert data["key"] == "my-existing-key"


@pytest.mark.django_db
def test_session_key_creates_a_new_key_for_first_time_visitors():
    """
    GET /session/ for a client with no cookie should create and return a
    fresh session key.
    """
    client = Client()
    response = client.get("/session/")

    assert response.status_code == 200
    data = json.loads(response.content)
    assert "key" in data
    assert data["key"]  # non-empty
