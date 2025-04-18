import pytest
from app.auth.service import (
    hash_password,
    verify_password,
    authenticate_user,
    change_user_password,
    request_password_reset,
    verify_password_reset,
    reset_tokens,
)
from app.auth.models import User
from app.auth.constants import UserRole


def create_test_user(email, password, db, role=UserRole.EXAMINER):
    hashed = hash_password(password)
    user = User(email=email, name="Test User", role=role, hashed_password=hashed)
    db.add(user)
    db.commit()
    return user


# --- Password Hashing ---
def test_hash_and_verify_password():
    pw = "securepass123"
    hashed = hash_password(pw)
    assert verify_password(pw, hashed)
    assert not verify_password("wrongpass", hashed)


# --- Login ---
def test_authenticate_user_success(db):
    email = "auth@test.com"
    password = "testpass"
    create_test_user(email, password, db)

    user = authenticate_user(email, password, db)
    assert user is not None
    assert user.email == email

def test_authenticate_user_failure(db):
    user = authenticate_user("nonexistent@x.com", "wrong", db)
    assert user is None


# --- Change Password ---
def test_change_user_password_success(db):
    email = "change@test.com"
    old_pw = "old123"
    new_pw = "new456"
    create_test_user(email, old_pw, db)

    updated_user = change_user_password(email, old_pw, new_pw, db)
    assert updated_user is not None
    assert verify_password(new_pw, updated_user.hashed_password)

def test_change_user_password_wrong_old_pw(db):
    email = "failchange@test.com"
    create_test_user(email, "original", db)

    updated_user = change_user_password(email, "wrongpass", "newpass", db)
    assert updated_user is None


# --- Password Reset ---
def test_request_password_reset_success(db):
    email = "reset@test.com"
    create_test_user(email, "resetme", db)

    assert request_password_reset(email, db)
    assert email in reset_tokens

def test_request_password_reset_invalid_email(db):
    assert not request_password_reset("noone@x.com", db)

def test_verify_password_reset_success(db):
    email = "reset2@test.com"
    create_test_user(email, "oldpw", db)
    request_password_reset(email, db)
    code = reset_tokens[email]

    success = verify_password_reset(email, code, "newpw", db)
    assert success is True

    # Confirm login with new password works
    user = authenticate_user(email, "newpw", db)
    assert user is not None

def test_verify_password_reset_invalid_code(db):
    email = "reset3@test.com"
    create_test_user(email, "startpw", db)
    request_password_reset(email, db)

    success = verify_password_reset(email, "999999", "newpw", db)
    assert success is False
