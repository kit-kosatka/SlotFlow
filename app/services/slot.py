from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Slot
from app.schemas.slot import SlotCreate
from app.repository.slot import SlotRepository


async def get_free_slots(session: AsyncSession) -> list[Slot]:
    repository = SlotRepository(session)
    return await repository.get_free_slots()


async def create_slot(slot_in: SlotCreate, session: AsyncSession) -> Slot:
    repository = SlotRepository(session)
    new_slot = Slot(
        specialist_id=slot_in.specialist_id, date=slot_in.date, time=slot_in.time
    )
    return await repository.create(new_slot)


async def delete_slot(slot_id: int, session: AsyncSession) -> dict[str, str]:
    repository = SlotRepository(session)
    slot = await repository.get_by_id(slot_id)
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    await repository.delete(slot)
    return {"message": "Slot deleted"}
