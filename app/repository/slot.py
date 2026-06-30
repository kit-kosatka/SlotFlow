from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Slot


class SlotRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_free_slots(self) -> list[Slot]:
        result = await self.session.execute(select(Slot).where(Slot.is_booked == False))
        return list(result.scalars().all())

    async def create(self, slot: Slot) -> Slot:
        self.session.add(slot)
        await self.session.commit()
        await self.session.refresh(slot)
        return slot

    async def get_by_id(self, slot_id: int) -> Slot | None:
        result = await self.session.execute(select(Slot).where(Slot.id == slot_id))
        return result.scalars().first()

    async def delete(self, slot: Slot) -> None:
        await self.session.delete(slot)
        await self.session.commit()
