from app.auth.models import User
from app.auth.constants import UserRole
from app.auth.service import hash_password


def test_create_user_model(db):
    user = User(
        email="testuser@x.com",
        name="Test User",
        role=UserRole.EXAMINER,
        hashed_password=hash_password("supersecret"),
        must_change_password=1
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.email == "testuser@x.com"
    assert user.role == UserRole.EXAMINER
    assert user.must_change_password == 1
    assert user.name == "Test User"
    assert user.hashed_password.startswith("$2b$")

