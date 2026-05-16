from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.associations import specialist_procedure


class Procedure(Base):
    __tablename__ = "procedures"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    duration: Mapped[int] = mapped_column()
    price: Mapped[int] = mapped_column()
    specialists: Mapped[list["Specialist"]] = relationship(
        secondary=specialist_procedure, back_populates="procedures"
    )
