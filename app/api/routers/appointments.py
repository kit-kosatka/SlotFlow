from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.db.session import get_db
from app.dependencies import get_current_user, require_role
from app.models import User, Slot, Appointment


router = APIRouter(prefix="/appointments", tags=["appointments"])

@router.post("/", response_model=AppointmentResponse)
async def create_appointment(
        appointment: AppointmentCreate,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Slot).where(Slot.id == appointment.slot_id))
    slot = result.scalars().first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    if slot.is_booked:
        raise HTTPException(status_code=400, detail="Slot already booked")
    new_appointment = Appointment(slot_id=appointment.slot_id, client_id=user.id, status="pending")
    slot.is_booked = True
    session.add(new_appointment)
    await session.commit()
    await session.refresh(new_appointment)
    return new_appointment


@router.get("/my", response_model=list[AppointmentResponse])
async def get_my_appointments(
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_db)
):
    result = await session.execute(select(Appointment).where(Appointment.client_id == user.id))
    appointments = result.scalars().all()
    return appointments

@router.delete("/{appointment_id}")
async def delete_appointment(
        appointment_id: int,
        user: User = Depends(require_role("admin")),
        session: AsyncSession = Depends(get_db)
):
    result = await session.execute(select(Appointment).where(Appointment.id == appointment_id))
    appointment = result.scalars().first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    slot_result = await session.execute(select(Slot).where(Slot.id == appointment.slot_id))
    slot = slot_result.scalars().first()
    slot.is_booked = False
    await session.delete(appointment)
    await session.commit()
    return {"message": "Appointment cancelled"}
