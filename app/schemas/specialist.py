from pydantic import BaseModel, ConfigDict


class SpecialistCreate(BaseModel):
    specialty: str
    description: str


class SpecialistResponse(BaseModel):
    id: int
    user_id: int
    specialty: str
    description: str

    model_config = ConfigDict(from_attributes=True)
