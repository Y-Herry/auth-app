from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ---------- 注册 ----------
class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    password: str = Field(..., min_length=6, description="密码（至少6位）")


# ---------- 登录 ----------
class LoginRequest(BaseModel):
    username: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., description="密码")


# ---------- 用户信息 ----------
class UserInfo(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class UserProfile(UserInfo):
    created_at: Optional[datetime] = None


# ---------- 响应 ----------
class RegisterResponse(BaseModel):
    code: int
    message: str
    data: Optional[UserInfo] = None


class LoginData(BaseModel):
    token: str
    user: UserInfo


class LoginResponse(BaseModel):
    code: int
    message: str
    data: Optional[LoginData] = None


class ProfileResponse(BaseModel):
    code: int
    message: str
    data: Optional[UserProfile] = None


class ErrorResponse(BaseModel):
    code: int
    message: str
