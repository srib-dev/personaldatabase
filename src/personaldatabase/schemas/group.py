from pydantic import BaseModel, ConfigDict
from datetime import date


# Filter for henting av data

class group_response(BaseModel):
    id: int
    group_name: str
    group_created_date: date | None


    model_config = ConfigDict(from_attributes=True)
