from pydantic import BaseModel, ConfigDict


# Skjema for å opprette nytt program
class ProgramCreate(BaseModel):
    program_name: str
    group_id: int
    is_active: bool = True


# Filter for henting av data
class ProgramResponse(BaseModel):
    id: int
    program_name: str
    group_id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
