from sqlalchemy import ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Appointment(Base):
    __tablename__ = 'appointments'
    id: Mapped[int] = mapped_column(primary_key=True)
    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.id"))
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(default="pending")
    slot: Mapped["Slot"] = relationship(back_populates="appointment")
    user: Mapped["User"] = relationship(back_populates="appointments")