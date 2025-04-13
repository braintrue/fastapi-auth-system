# schemas.py
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: int
    email: str
    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str  # ✅ 추가!
    token_type: str

class UserInfo(BaseModel):
    email: str

class TokenRefresh(BaseModel):
    refresh_token: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None