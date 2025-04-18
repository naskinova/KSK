import pytest
from datetime import timedelta, datetime

from app.auth.security import create_access_token, decode_access_token
from app.auth.constants import UserRole
import jwt


def test_create_and_decode_token_success():
    data = {"sub": "123", "role": UserRole.EXAMINER}
    token = create_access_token(data)

    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "123"
    assert decoded["role"] == "examiner"
    assert "exp" in decoded


def test_create_token_with_custom_expiration():
    data = {"sub": "456", "role": UserRole.WEB_ADMIN}
    expire_in = timedelta(minutes=5)
    token = create_access_token(data, expires_delta=expire_in)

    decoded = decode_access_token(token)
    assert decoded["sub"] == "456"
    assert decoded["role"] == "web_admin"


def test_expired_token_is_invalid(monkeypatch):
    # Monkeypatch datetime to simulate past expiration
    from app.auth import security

    # Token with -1 second expiry
    data = {"sub": "789", "role": UserRole.REPORT_ADMIN}
    token = create_access_token(data, expires_delta=timedelta(seconds=-1))

    decoded = decode_access_token(token)
    assert decoded is None


def test_invalid_token_returns_none():
    invalid_token = "this.is.not.a.jwt"
    result = decode_access_token(invalid_token)
    assert result is None
