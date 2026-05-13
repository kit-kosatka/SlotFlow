from pydantic import BaseModel, ConfigDict

class AppointmentCreate(BaseModel):
    slot_id: int

class AppointmentResponse(BaseModel):
    id: int
    slot_id: int
    client_id: int
    status: str

    model_config = ConfigDict(from_attributes=True)