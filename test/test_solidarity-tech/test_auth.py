from __future__ import annotations

import secrets

import requests

from parsons.solidarity_tech.auth import SolidarityTechAuth


def test_auth_init() -> None:
    """Test that the auth object is initialized with the supplied API key."""
    api_token = secrets.token_hex(64)
    auth = SolidarityTechAuth(api_token)
    assert auth.api_key == api_token


def test_auth_eq() -> None:
    """Test that instances of auth objects with the same API key can be compared for equality."""
    api_token = secrets.token_hex(64)
    auth1 = SolidarityTechAuth(api_token)
    auth2 = SolidarityTechAuth(api_token)
    assert auth1 == auth2


def test_auth_hash() -> None:
    """Test that auth objects are hashable based on their API key and can be used as dictionary keys."""
    api_token = secrets.token_hex(64)
    auth = SolidarityTechAuth(api_token)
    assert hash(auth) == hash(api_token)


def test_auth_repr() -> None:
    """Test that auth objects include the API key in their repr."""
    api_token = secrets.token_hex(64)
    auth = SolidarityTechAuth(api_token)
    assert api_token in repr(auth)


def test_auth_call() -> None:
    """Test that calling an auth object with a request adds the authorization header."""
    api_token = secrets.token_hex(64)
    auth = SolidarityTechAuth(api_token)
    req = requests.Request(url="https://example.com")
    req = req.prepare()
    auth(req)
    assert req.headers["authorization"] == f"Bearer {api_token}"


def test_auth_call_does_not_clear_headers() -> None:
    """Test that calling an auth object with a request adds the authorization header to existing headers."""
    api_token = secrets.token_hex(64)
    auth = SolidarityTechAuth(api_token)
    req = requests.Request(url="https://example.com", headers={"X-Test": "test"})
    req = req.prepare()
    auth(req)
    assert req.headers["authorization"] == f"Bearer {api_token}"
    assert req.headers["X-Test"] == "test"
