from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Specialist
from sqlalchemy import select


class SpecialistRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> list[Specialist]:
        result = await self.session.execute(select(Specialist))
        return list(result.scalars().all())

    async def get_by_id(self, specialist_id: int) -> Specialist | None:
        result = await self.session.execute(
            select(Specialist).where(Specialist.id == specialist_id)
        )
        return result.scalars().first()

    async def create(self, specialist: Specialist) -> Specialist:
        self.session.add(specialist)
        await self.session.commit()
        await self.session.refresh(specialist)
        return specialist
