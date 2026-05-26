from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models import User, Appointment, Slot
from app.schemas.appointment import AppointmentCreate
from sqlalchemy import select


async def create_appointment(
    appointment: AppointmentCreate,
    user: User,
    session: AsyncSession,
) -> Appointment:
    result = await session.execute(select(Slot).where(Slot.id == appointment.slot_id))
    slot = result.scalars().first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    if slot.is_booked:
        raise HTTPException(status_code=400, detail="Slot already booked")
    new_appointment = Appointment(
        slot_id=appointment.slot_id, client_id=user.id, status="pending"
    )
    slot.is_booked = True
    session.add(new_appointment)
    await session.commit()
    await session.refresh(new_appointment)
    return new_appointment


async def get_my_appointments(user: User, session: AsyncSession) -> list[Appointment]:
    result = await session.execute(
        select(Appointment).where(Appointment.client_id == user.id)
    )
    appointments = result.scalars().all()
    return appointments


async def delete_appointment(
    appointment_id: int,
    session: AsyncSession,
) -> dict[str, str]:
    result = await session.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    )
    appointment = result.scalars().first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    slot_result = await session.execute(
        select(Slot).where(Slot.id == appointment.slot_id)
    )
    slot = slot_result.scalars().first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    slot.is_booked = False
    await session.delete(appointment)
    await session.commit()
    return {"message": "Appointment cancelled"}
