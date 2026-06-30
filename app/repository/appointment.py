from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, Appointment
from sqlalchemy import select


class AppointmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, appointment: Appointment) -> Appointment:
        self.session.add(appointment)
        await self.session.commit()
        await self.session.refresh(appointment)
        return appointment

    async def get_my_appointments(self, user: User) -> list[Appointment]:
        result = await self.session.execute(
            select(Appointment).where(Appointment.client_id == user.id)
        )
        appointments = result.scalars().all()
        return list(appointments)

    async def get_by_id(self, appointment_id: int) -> Appointment | None:
        result = await self.session.execute(
            select(Appointment).where(Appointment.id == appointment_id)
        )
        return result.scalars().first()

    async def delete(self, appointment: Appointment) -> None:
        await self.session.delete(appointment)
        await self.session.commit()
