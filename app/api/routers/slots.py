from fastapi import APIRouter, Depends
from app.schemas.slot import SlotCreate, SlotResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models import Slot, User
from app.dependencies import require_role
from app.services.slot import get_free_slots, create_slot, delete_slot

router = APIRouter(prefix="/slots", tags=["slots"])


@router.get("/", response_model=list[SlotResponse])
async def get_slots_route(session: AsyncSession = Depends(get_db)):
    return await get_free_slots(session)


@router.post("/", response_model=SlotResponse)
async def create_slot_route(
    slot: SlotCreate,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("specialist")),
):
    return await create_slot(slot, session)


@router.delete("/{slot_id}")
async def delete_slot_route(
    slot_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("specialist")),
):
   return await delete_slot(slot_id, session)
