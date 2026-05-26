from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.db.session import get_db
from app.dependencies import get_current_user, require_role
from app.models import User
from app.services.appointment import (
    create_appointment,
    delete_appointment,
    get_my_appointments,
)

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("/", response_model=AppointmentResponse)
async def create_appointment_route(
    appointment: AppointmentCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    return await create_appointment(appointment, user, session)


@router.get("/my", response_model=list[AppointmentResponse])
async def get_my_appointments_route(
    user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)
):
    return await get_my_appointments(user, session)


@router.delete("/{appointment_id}")
async def delete_appointment_route(
    appointment_id: int,
    user: User = Depends(require_role("admin")),
    session: AsyncSession = Depends(get_db),
):
    return await delete_appointment(appointment_id, session)
