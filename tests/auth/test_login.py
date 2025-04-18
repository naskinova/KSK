from app.auth.models import User
from app.auth.constants import UserRole
from app.auth.service import hash_password

def test_login_success(client, db):
    pw = hash_password("examiner123")
    user = User(email="examiner@domain.com", name="Test Examiner", role=UserRole.EXAMINER, hashed_password=pw)
    db.add(user)
    db.commit()

    response = client.post("/auth/login", json={"email": user.email, "password": "examiner123"})

    assert response.status_code == 200
    assert response.json()["user"]["role"] == "examiner"

