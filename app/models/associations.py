from sqlalchemy import Table, Column, ForeignKey
from app.db.base import Base

specialist_procedure = Table(
    "specialist_procedure",
    Base.metadata,
    Column("specialist_id", ForeignKey("specialists.id"), primary_key=True),
    Column("procedure_id", ForeignKey("procedures.id"), primary_key=True),
)
