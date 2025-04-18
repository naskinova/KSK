from pydantic import BaseModel, EmailStr
from app.auth.constants import UserRole

# Request body for /auth/login
class LoginInput(BaseModel):
    email: EmailStr
    password: str

# Response body for successful login
class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: UserRole
    must_change_password: bool

    model_config = {
        "from_attributes": True
    }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

# Request body for changing password (authenticated)
class ChangePasswordInput(BaseModel):
    email: EmailStr
    old_password: str
    new_password: str

# Request body for forgot password (send reset code)
class PasswordResetRequest(BaseModel):
    email: EmailStr

# Request body for verifying reset code and setting new password
class PasswordResetVerify(BaseModel):
    email: EmailStr
    code: str
    new_password: str
