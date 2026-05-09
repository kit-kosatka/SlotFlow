from sqlalchemy import ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.associations import specialist_procedure

class Specialist(Base):
    __tablename__ = "specialists"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    specialty: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    user: Mapped["User"] = relationship(back_populates="specialist")
    slots: Mapped[list["Slot"]] = relationship(back_populates="specialist")
    procedures: Mapped[list["Procedure"]] = relationship(secondary=specialist_procedure, back_populates="specialists")
