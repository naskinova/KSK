import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from app.auth.dependencies import get_current_user
from app.auth.security import create_access_token
from app.auth.models import User
from app.auth.service import hash_password
from app.auth.constants import UserRole


def create_user(db, email="tokenuser@x.com", password="test123", role=UserRole.EXAMINER):
    user = User(
        email=email,
        name="Token User",
        role=role,
        hashed_password=hash_password(password),
        must_change_password=0
    )
    db.add(user)
    db.commit()
    return user


def build_protected_test_app():
    app = FastAPI()

    @app.get("/protected")
    def protected(user=Depends(get_current_user)):
        return {"email": user.email, "role": user.role}

    return app


def test_get_current_user_success(db):
    user = create_user(db)
    token = create_access_token({"sub": str(user.id), "role": user.role})

    app = build_protected_test_app()
    client = TestClient(app)

    res = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["email"] == user.email


def test_get_current_user_invalid_format(db):
    app = build_protected_test_app()
    client = TestClient(app)

    res = client.get("/protected", headers={"Authorization": "Token abcdef"})
    assert res.status_code == 401
    assert res.json()["detail"] == "Invalid token format"


def test_get_current_user_expired_or_invalid_token(db):
    app = build_protected_test_app()
    client = TestClient(app)

    res = client.get("/protected", headers={"Authorization": "Bearer invalid.token.here"})
    assert res.status_code == 401
    assert res.json()["detail"] == "Invalid or expired token"


def test_get_current_user_user_not_found(db):
    token = create_access_token({"sub": "9999", "role": "examiner"})  # Non-existent user ID

    app = build_protected_test_app()
    client = TestClient(app)

    res = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 404
    assert res.json()["detail"] == "User not found"
