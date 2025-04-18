from fastapi import Depends, HTTPException, Header
from app.auth.security import decode_access_token
from app.database.session import get_db
from app.auth.models import User
from sqlalchemy.orm import Session


def get_current_user(
        authorization: str = Header(..., alias="Authorization"),
        db: Session = Depends(get_db)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.split(" ")[1]
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token missing user ID")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
