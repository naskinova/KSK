import random
from typing import Optional

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.auth.models import User
from app.utils.email import send_login_code  # Make sure this function exists

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Password Hashing ---
def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """Check if the provided password matches the hashed password."""
    return pwd_context.verify(plain, hashed)

# --- Login ---
def authenticate_user(email: str, password: str, db: Session) -> Optional[User]:
    """Authenticate a user by email and password."""
    user = db.query(User).filter_by(email=email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# --- Change Password ---
def change_user_password(email: str, old_pw: str, new_pw: str, db: Session) -> Optional[User]:
    """Change a user's password after verifying the old one."""
    user = db.query(User).filter_by(email=email).first()
    if not user or not verify_password(old_pw, user.hashed_password):
        return None
    user.hashed_password = hash_password(new_pw)
    user.must_change_password = 0
    db.commit()
    return user

# --- Password Reset (Temporary In-Memory Store) ---
reset_tokens: dict[str, str] = {}  # {email: code}, use Redis or DB in production

def request_password_reset(email: str, db: Session) -> bool:
    """Send a reset code to the user's email."""
    user = db.query(User).filter_by(email=email).first()
    if not user:
        return False
    code = str(random.randint(100000, 999999))
    reset_tokens[email] = code
    send_login_code(email, code)
    return True

def verify_password_reset(email: str, code: str, new_password: str, db: Session) -> bool:
    """Verify the reset code and update the user's password."""
    if reset_tokens.get(email) != code:
        return False
    user = db.query(User).filter_by(email=email).first()
    if not user:
        return False
    user.hashed_password = hash_password(new_password)
    db.commit()
    del reset_tokens[email]
    return True
