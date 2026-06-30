from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models import User, Appointment
from app.schemas.appointment import AppointmentCreate
from app.repository.appointment import AppointmentRepository
from app.repository.slot import SlotRepository


async def create_appointment(
    appointment: AppointmentCreate,
    user: User,
    session: AsyncSession,
) -> Appointment:
    repo_appointment = AppointmentRepository(session)
    repo_slot = SlotRepository(session)
    slot = await repo_slot.get_by_id(appointment.slot_id)
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    if slot.is_booked:
        raise HTTPException(status_code=400, detail="Slot already booked")
    slot.is_booked = True
    new_appointment = Appointment(
        slot_id=appointment.slot_id, client_id=user.id, status="pending"
    )
    new_appointment = await repo_appointment.create(new_appointment)
    return new_appointment


async def get_my_appointments(user: User, session: AsyncSession) -> list[Appointment]:
    repo_appointment = AppointmentRepository(session)
    return await repo_appointment.get_my_appointments(user)


async def delete_appointment(
    appointment_id: int,
    session: AsyncSession,
) -> dict[str, str]:
    repo_appointment = AppointmentRepository(session)
    repo_slot = SlotRepository(session)
    appointment = await repo_appointment.get_by_id(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    slot = await repo_slot.get_by_id(appointment.slot_id)
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    slot.is_booked = False
    await repo_appointment.delete(appointment)
    return {"message": "Appointment cancelled"}
