from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserRegister, UserLogin, TokenResponse
from app.services.auth import register, login

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register_route(user: UserRegister, session: AsyncSession = Depends(get_db)):
    return await register(user, session)


@router.post("/login", response_model=TokenResponse)
async def login_route(user: UserLogin, session: AsyncSession = Depends(get_db)):
    return await login(user, session)
