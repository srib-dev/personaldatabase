from datetime import date

from pydantic import BaseModel, ConfigDict


# Filter for henting av data

class group_response(BaseModel):
    id: int
    group_name: str
    group_created_date: date

    model_config = ConfigDict(from_attributes=True)
