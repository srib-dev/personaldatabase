
from datetime import date

from pydantic import BaseModel, ConfigDict, Field



class GroupMemberAdd(BaseModel):
    person_id: int
    when_joined_group: date = Field(default_factory=date.today)
    
class GroupMemberResponse(BaseModel):
    person_id: int
    group_id: int
    when_joined_group: date
    model_config = ConfigDict(from_attributes=True)