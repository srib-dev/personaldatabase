from pydantic import BaseModel, ConfigDict


class ProgramMemberAdd(BaseModel):
    person_id: int
    program_role: str


class ProgramMemberResponse(BaseModel):
    program_role: str

    model_config = ConfigDict(from_attributes=True)
