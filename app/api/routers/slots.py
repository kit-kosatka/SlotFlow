from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.schemas.slot import SlotCreate, SlotResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models import Slot, User
from app.dependencies import require_role

router = APIRouter(prefix="/slots", tags=["slots"])


@router.get("/", response_model=list[SlotResponse])
async def get_slots(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Slot).where(Slot.is_booked == False))
    return result.scalars().all()


@router.post("/", response_model=SlotResponse)
async def create_slot(
    slot: SlotCreate,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("specialist")),
):
    new_slot = Slot(specialist_id=slot.specialist_id, date=slot.date, time=slot.time)
    session.add(new_slot)
    await session.commit()
    await session.refresh(new_slot)
    return new_slot


@router.delete("/{slot_id}")
async def delete_slot(
    slot_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("specialist")),
):
    result = await session.execute(select(Slot).where(Slot.id == slot_id))
    slot = result.scalars().first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    await session.delete(slot)
    await session.commit()
    return {"message": "Slot deleted"}
