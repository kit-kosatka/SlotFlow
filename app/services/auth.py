from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserRegister, UserLogin
from app.core.security import create_token
from app.models import User
from app.core.security import hash_password, verify_password
from app.repository.user import UserRepository


async def register(user: UserRegister, session: AsyncSession) -> dict[str, str]:
    repository = UserRepository(session)
    user_in = await repository.get_by_email(user.email)
    if user_in:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    new_user = User(
        name=user.name, email=user.email, password_hash=hashed_password, role=user.role
    )
    await repository.create(new_user)
    return {"message": "Registered successfully"}


async def login(user: UserLogin, session: AsyncSession) -> dict[str, str]:
    repository = UserRepository(session)
    user_in = await repository.get_by_email(user.username)
    if not user_in or not verify_password(user.password, user_in.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_token(user_in.id)
    return {"access_token": token, "token_type": "bearer"}
