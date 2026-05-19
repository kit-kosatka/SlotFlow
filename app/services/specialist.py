from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.specialist import SpecialistCreate, SpecialistResponse
from app.models import Specialist
from sqlalchemy import select


async def get_all(session: AsyncSession) -> list[SpecialistResponse]:
    result = await session.execute(select(Specialist))
    return list(result.scalars().all())

async def get_by_id(specialist_id: int, session: AsyncSession) -> SpecialistResponse:
    result = await session.execute(select(Specialist).where(Specialist.id == specialist_id))
    specialist_in = result.scalars().first()
    if not specialist_in:
        raise HTTPException(status_code=404, detail="Specialist not found")
    return specialist_in

async def create_specialist(specialist_in: SpecialistCreate, user_id: int, session: AsyncSession) -> SpecialistResponse:
    new_specialist = Specialist(user_id=user_id, specialty=specialist_in.specialty, description=specialist_in.description)
    session.add(new_specialist)
    await session.commit()
    await session.refresh(new_specialist)
    return new_specialist