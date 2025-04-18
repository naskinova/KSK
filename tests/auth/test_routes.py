from app.auth.models import User
from app.auth.service import hash_password, reset_tokens
from app.auth.constants import UserRole


def create_user(email, password, db, role=UserRole.EXAMINER):
    user = User(
        email=email,
        name="Test User",
        role=role,
        hashed_password=hash_password(password),
        must_change_password=0
    )
    db.add(user)
    db.commit()
    return user


def test_login_route_success(client, db):
    user = create_user("login@x.com", "123456", db)
    response = client.post("/auth/login", json={"email": user.email, "password": "123456"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == user.email


def test_login_route_failure(client, db):
    response = client.post("/auth/login", json={"email": "fail@x.com", "password": "wrong"})
    assert response.status_code == 401


def test_request_reset_route_success(client, db):
    user = create_user("reset@x.com", "reset123", db)
    response = client.post("/auth/request-reset", json={"email": user.email})
    assert response.status_code == 200
    assert "message" in response.json()
    assert user.email in reset_tokens


def test_request_reset_route_invalid_email(client, db):
    response = client.post("/auth/request-reset", json={"email": "noone@nowhere.com"})
    assert response.status_code == 404


def test_verify_reset_route_success(client, db):
    user = create_user("verify@x.com", "oldpw", db)
    client.post("/auth/request-reset", json={"email": user.email})
    code = reset_tokens[user.email]

    response = client.post("/auth/verify-reset", json={
        "email": user.email,
        "code": code,
        "new_password": "newpw"
    })
    assert response.status_code == 200
    assert "message" in response.json()

    # Confirm login with new password works
    login = client.post("/auth/login", json={"email": user.email, "password": "newpw"})
    assert login.status_code == 200


def test_verify_reset_route_invalid_code(client, db):
    user = create_user("wrongcode@x.com", "start", db)
    client.post("/auth/request-reset", json={"email": user.email})

    response = client.post("/auth/verify-reset", json={
        "email": user.email,
        "code": "123456",
        "new_password": "new"
    })
    assert response.status_code == 400


def test_get_logged_in_user(client, db):
    user = create_user("me@x.com", "passme", db)
    login = client.post("/auth/login", json={"email": user.email, "password": "passme"})
    assert login.status_code == 200
    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    me = client.get("/auth/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["user"]["email"] == user.email
    assert me.json()["user"]["role"] == "examiner"
