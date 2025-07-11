from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    role: str
    force_password_change: Optional[bool] = False

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    full_name: Optional[str]
    role: str
    created_at: datetime
    password: Optional[str]
    model_config = {
        "from_attributes": True
    }

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    role: str
    password: str

class UserUpdate(BaseModel):
    email: EmailStr
    full_name: str
    role: str
    password: Optional[str] = Field(default=None, min_length=8)

class ChangePasswordSchema(BaseModel):
    current_password: str
    new_password: str
    
class GoogleLoginRequest(BaseModel):
    id_token: str

