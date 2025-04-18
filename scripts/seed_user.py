import sys
import os

# Ensure app/ is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.auth.models import User
from app.auth.constants import UserRole
from app.auth.service import hash_password
from app.database.session import SessionLocal

def seed_users():
    db = SessionLocal()

    users_to_seed = [
        {
            "email": "admin@ksk.com",
            "name": "Admin User",
            "role": UserRole.WEB_ADMIN,
            "password": "admin123"
        },
        {
            "email": "examiner1@ksk.com",
            "name": "Examiner One",
            "role": UserRole.EXAMINER,
            "password": "examiner123"
        },
        {
            "email": "report@ksk.com",
            "name": "Report Admin",
            "role": UserRole.REPORT_ADMIN,
            "password": "report123"
        }
    ]

    for user_data in users_to_seed:
        existing = db.query(User).filter_by(email=user_data["email"]).first()
        if existing:
            print(f"⚠️  User already exists: {existing.email}")
            continue

        user = User(
            email=user_data["email"],
            name=user_data["name"],
            role=user_data["role"],
            hashed_password=hash_password(user_data["password"]),
            must_change_password=0
        )
        db.add(user)
        print(f"✅ Added: {user.email}")

    db.commit()
    db.close()
    print("✅ Done seeding users.")

if __name__ == "__main__":
    seed_users()
