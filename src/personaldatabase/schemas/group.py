from datetime import date

from pydantic import BaseModel, ConfigDict, Field


# Skjema for å opprette ny gruppe
class GroupCreate(BaseModel):
    group_name: str
    group_created_date: date = Field(default_factory=date.today)


# Filter for henting av data
class GroupResponse(BaseModel):
    id: int
    group_name: str
    group_created_date: date

    model_config = ConfigDict(from_attributes=True)