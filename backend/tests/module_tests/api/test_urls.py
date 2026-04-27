"""
Tests for api/server/urls.py.

Every HTTP path that the frontend calls must resolve to the right named view.
These tests act as a registry check — if a path is removed or renamed on the
backend, the test fails immediately rather than silently breaking the frontend.
"""

import pytest
from django.urls import resolve, reverse, NoReverseMatch


# All HTTP paths used by the frontend (from src/utilities/api.ts)
FRONTEND_HTTP_ROUTES = [
    ("",         "get_network"),   # GET /
    ("bias/",    "bias"),          # GET /bias/
    ("condition/", "condition"),   # POST /condition/
    ("csrf/",    "csrf"),          # GET /csrf/
    ("session/", "session"),       # GET /session/
]


@pytest.mark.django_db
@pytest.mark.parametrize("path,expected_name", FRONTEND_HTTP_ROUTES)
def test_path_resolves_to_the_right_named_view(path, expected_name):
    """
    Every path the frontend uses must resolve to the named view we expect.
    A mismatch means the URL has been moved without updating the frontend.
    """
    match = resolve(f"/{path}")
    assert match.url_name == expected_name, (
        f"/{path} resolved to '{match.url_name}', expected '{expected_name}'"
    )


@pytest.mark.django_db
@pytest.mark.parametrize("path,name", FRONTEND_HTTP_ROUTES)
def test_named_view_can_be_reversed_to_its_path(path, name):
    """
    Every named view must be reversible.  If a view name is removed from
    urlpatterns, reverse() will raise NoReverseMatch and the test fails.
    """
    try:
        reversed_path = reverse(name).lstrip("/")
        assert reversed_path == path
    except NoReverseMatch:
        pytest.fail(f"View name '{name}' cannot be reversed — is it missing from urls.py?")


@pytest.mark.django_db
def test_condition_with_predefined_id_also_resolves():
    """
    The condition view has an optional <predefined> parameter used by the
    walkthrough pages to condition named networks like the sprinkler network.
    """
    match = resolve("/condition/sprinkler/")
    assert match.url_name == "condition_with_id"
    assert match.kwargs == {"predefined": "sprinkler"}
