from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Body

from app.auth.schemas import LoginInput, TokenResponse, PasswordResetRequest, PasswordResetVerify
from app.auth.service import authenticate_user, request_password_reset, verify_password_reset, hash_password
from app.auth.security import create_access_token
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.auth.models import User

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(data: LoginInput, db: Session = Depends(get_db)):
    user = authenticate_user(data.email, data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "must_change_password": bool(user.must_change_password),
        }
    }

@router.post("/request-reset")
def request_reset(data: PasswordResetRequest, db: Session = Depends(get_db)):
    if not request_password_reset(data.email, db):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Reset code sent"}

@router.post("/verify-reset")
def verify_reset(data: PasswordResetVerify = Body(...), db: Session = Depends(get_db)):
    if not verify_password_reset(data.email, data.code, data.new_password, db):
        raise HTTPException(status_code=400, detail="Invalid reset attempt")
    return {"message": "Password reset successful"}

@router.get("/me", response_model=TokenResponse)
def get_logged_in_user(user: User = Depends(get_current_user)):
    access_token = create_access_token({"sub": str(user.id), "role": user.role})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "must_change_password": bool(user.must_change_password),
        }
    }
