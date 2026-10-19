from pydantic import BaseModel, ConfigDict


class VervMemberAdd(BaseModel):
    person_id: int


class VervMemberResponse(BaseModel):
    person_id: int
    verv_id: int

    model_config = ConfigDict(from_attributes=True)


# Aliases
PersonVervAdd = VervMemberAdd
PersonVervResponse = VervMemberResponse
