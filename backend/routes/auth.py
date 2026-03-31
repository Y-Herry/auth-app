from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from config.database import get_db
from models.user import User
from schemas.auth import (
    RegisterRequest, RegisterResponse,
    LoginRequest, LoginResponse, LoginData,
    ProfileResponse, UserInfo, UserProfile
)
from utils.security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=RegisterResponse, status_code=201, summary="用户注册")
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    # 检查用户名或邮箱是否已存在
    existing = db.query(User).filter(
        or_(User.username == body.username, User.email == body.email)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="用户名或邮箱已被注册"
        )

    # 创建新用户
    new_user = User(
        username=body.username,
        email=body.email,
        password=hash_password(body.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RegisterResponse(
        code=201,
        message="注册成功",
        data=UserInfo(id=new_user.id, username=new_user.username, email=new_user.email)
    )


@router.post("/login", response_model=LoginResponse, status_code=200, summary="用户登录")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    # 支持用户名或邮箱登录
    user = db.query(User).filter(
        or_(User.username == body.username, User.email == body.username)
    ).first()

    if not user or not verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    # 生成 JWT Token
    token = create_access_token(data={
        "id": user.id,
        "username": user.username,
        "email": user.email
    })

    return LoginResponse(
        code=200,
        message="登录成功",
        data=LoginData(
            token=token,
            user=UserInfo(id=user.id, username=user.username, email=user.email)
        )
    )


@router.get("/profile", response_model=ProfileResponse, status_code=200, summary="获取当前用户信息")
def get_profile(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user["id"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    return ProfileResponse(
        code=200,
        message="获取成功",
        data=UserProfile(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at
        )
    )
