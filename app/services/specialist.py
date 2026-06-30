from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.specialist import SpecialistCreate
from app.models import Specialist
from app.repository.specialist import SpecialistRepository


async def get_all(session: AsyncSession) -> list[Specialist]:
    repository = SpecialistRepository(session)
    return await repository.get_all()


async def get_by_id(specialist_id: int, session: AsyncSession) -> Specialist:
    repository = SpecialistRepository(session)
    specialist_in = await repository.get_by_id(specialist_id)
    if not specialist_in:
        raise HTTPException(status_code=404, detail="Specialist not found")
    return specialist_in


async def create_specialist(
    specialist_in: SpecialistCreate, user_id: int, session: AsyncSession
) -> Specialist:
    repository = SpecialistRepository(session)
    new_specialist = Specialist(
        user_id=user_id,
        specialty=specialist_in.specialty,
        description=specialist_in.description,
    )
    return await repository.create(new_specialist)
