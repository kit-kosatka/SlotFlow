from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.specialist import SpecialistCreate, SpecialistResponse
from app.db.session import get_db
from app.dependencies import require_role
from app.models import User
from app.services.specialist import get_all, create_specialist, get_by_id

router = APIRouter(prefix="/specialists", tags=["specialists"])


@router.get("/", response_model=list[SpecialistResponse])
async def get_specialists(session: AsyncSession = Depends(get_db)):
    return await get_all(session)


@router.get("/{specialist_id}", response_model=SpecialistResponse)
async def get_specialist(
    specialist_id: int, session: AsyncSession = Depends(get_db)):
    return await get_by_id(specialist_id, session)


@router.post("/", response_model=SpecialistResponse)
async def create_specialist(specialist_in: SpecialistCreate, user_id: int, session: AsyncSession = Depends(get_db), user: User = Depends(require_role("admin"))):
    return await create_specialist(specialist_in, user_id, session)
