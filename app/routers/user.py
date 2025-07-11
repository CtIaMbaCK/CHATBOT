from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.database import get_db
from app.db.models.user_model import User
from app.db.schemas.user_schema import UserCreate, UserUpdate, UserOut
from app.core.security import password

from app.core.security import get_current_user

router = APIRouter(tags=["Users"])

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

@router.get("/all-users", response_model=List[UserOut])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

@router.post("/create")
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    # result = await db.execute(select(User).where(User.id == data.id))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email đã tồn tại")

    user = User(
        email=data.email,
        full_name=data.full_name,
        role=data.role,
        password=password(data.password)  # dùng hàm password() không mã hóa
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {
        "message": " Tạo người dùng thành công",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "created_at": user.created_at
        }
    }

@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: UUID, data: UserUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Người dùng không tồn tại")

    user.full_name = data.full_name
    user.email = data.email
    user.role = data.role

    if data.password:  # Nếu có cập nhật mật khẩu
        user.password = data.password  # Không mã hóa, dùng password trực tiếp

    await db.commit()
    await db.refresh(user)

    return user

@router.get("/current")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {
        "user_id": current_user.id,
        "username": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role,
    }

@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {
        "message": "Hello, bạn đã đăng nhập thành công!",
        "user_id": current_user.id,
        "role": current_user.role,
    }
