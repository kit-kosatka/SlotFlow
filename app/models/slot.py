from typing import Optional
from sqlalchemy import ForeignKey
from datetime import date, time
from app.db.base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Slot(Base):
    __tablename__ = 'slots'
    id: Mapped[int] = mapped_column(primary_key=True)
    specialist_id: Mapped[int] = mapped_column(ForeignKey('specialists.id'))
    date: Mapped[date] = mapped_column()
    time: Mapped[time] = mapped_column()
    is_booked: Mapped[bool] = mapped_column(default=False)
    specialist: Mapped["Specialist"] = relationship(back_populates="slots")
    appointment: Mapped[Optional["Appointment"]] = relationship(back_populates="slot")
