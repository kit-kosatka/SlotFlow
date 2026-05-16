from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models import User
from app.schemas.user import UserRegister, UserLogin, TokenResponse
from app.core.security import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(user: UserRegister, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        role=user.role,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return {"message": "Registered successfully"}


@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(User).where(User.email == user.username))
    existing_user = result.scalars().first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="Email not registered")
    user_password = verify_password(user.password, existing_user.password_hash)
    if not user_password:
        raise HTTPException(status_code=400, detail="Incorrect")
    token = create_token(existing_user.id)
    return {"access_token": token, "token_type": "bearer"}
