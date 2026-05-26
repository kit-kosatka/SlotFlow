from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Slot
from app.schemas.slot import SlotCreate


async def get_free_slots(session: AsyncSession) -> list[Slot]:
    result = await session.execute(select(Slot).where(Slot.is_booked == False))
    return result.scalars().all()


async def create_slot(slot_in: SlotCreate, session: AsyncSession) -> Slot:
    new_slot = Slot(
        specialist_id=slot_in.specialist_id, date=slot_in.date, time=slot_in.time
    )
    session.add(new_slot)
    await session.commit()
    await session.refresh(new_slot)
    return new_slot


async def delete_slot(slot_id: int, session: AsyncSession) -> dict[str, str]:
    result = await session.execute(select(Slot).where(Slot.id == slot_id))
    slot = result.scalars().first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    await session.delete(slot)
    await session.commit()
    return {"message": "Slot deleted"}
