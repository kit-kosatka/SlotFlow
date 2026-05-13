from datetime import date as date_, time as time_
from pydantic import BaseModel, ConfigDict


class SlotCreate(BaseModel):
    specialist_id: int
    date: date_
    time: time_

class SlotResponse(BaseModel):
    id: int
    specialist_id: int
    date: date_
    time: time_

    model_config = ConfigDict(from_attributes=True)







