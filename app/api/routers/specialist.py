from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.specialist import SpecialistCreate, SpecialistResponse
from app.db.session import get_db
from app.models import Specialist
from app.dependencies import require_role
from app.models import User

router = APIRouter(prefix="/specialists", tags=["specialists"])

@router.get("/", response_model=list[SpecialistResponse])
async def get_specialists(session: AsyncSession = Depends(get_db)) -> list:
    result = await session.execute(select(Specialist))
    return result.scalars().all()

@router.get("/{specialist_id}", response_model=SpecialistResponse)
async def get_specialist(specialist_id: int, session: AsyncSession = Depends(get_db)) -> SpecialistResponse:
    result = await session.execute(select(Specialist).where(Specialist.id == specialist_id))
    specialist = result.scalars().first()
    if specialist is None:
        raise HTTPException(status_code=404, detail="Specialist not found")
    return specialist

@router.post("/", response_model=SpecialistResponse)
async def create_specialist(
        specialist_in: SpecialistCreate,
        user_id: int,
        session: AsyncSession = Depends(get_db),
        user: User = Depends(require_role("admin"))) -> SpecialistResponse:
    new_specialist = Specialist(user_id=user_id, specialty=specialist_in.specialty, description=specialist_in.description)
    session.add(new_specialist)
    await session.commit()
    await session.refresh(new_specialist)
    return new_specialist
