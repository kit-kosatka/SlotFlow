from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserRegister, UserLogin
from app.core.security import create_token
from app.models import User
from sqlalchemy import select
from app.core.security import hash_password, verify_password


async def register(user: UserRegister, session: AsyncSession):
    result = await session.execute(select(User).where(User.email == user.email))
    user_in = result.scalars().first()
    if user_in:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    new_user = User(name=user.name, email=user.email, password_hash=hashed_password, role=user.role)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return {"message": "Registered successfully"}

async def login(user: UserLogin, session: AsyncSession):
    result = await session.execute(select(User).where(User.email == user.username))
    user_in = result.scalars().first()
    if not user_in or not verify_password(user.password, user_in.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_token(user_in.id)
    return {"access_token": token, "token_type": "bearer"}
