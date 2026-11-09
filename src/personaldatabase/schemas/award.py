from pydantic import BaseModel, ConfigDict

from personaldatabase.schemas.person import person_response
from personaldatabase.schemas.program import ProgramResponse


class AwardCreate(BaseModel):
    award_name: str
    description: str | None = None
    is_program_award: bool = False


class AwardUpdate(BaseModel):
    award_name: str | None = None
    description: str | None = None
    is_program_award: bool | None = None


class AwardResponse(BaseModel):
    id: int
    award_name: str
    description: str | None = None
    is_program_award: bool

    model_config = ConfigDict(from_attributes=True)


class AwardWinCreate(BaseModel):
    semester: str
    program_id: int | None = None
    note: str | None = None
    person_ids: list[int] | None = None
    copy_program_members: bool | None = None


class AwardWinPersonResponse(BaseModel):
    award_win_id: int
    person_id: int

    model_config = ConfigDict(from_attributes=True)


class AwardWinResponse(BaseModel):
    id: int
    award_id: int
    semester: str
    program_id: int | None = None
    note: str | None = None
    award: AwardResponse
    program: ProgramResponse | None = None
    winners: list[person_response] = []

    model_config = ConfigDict(from_attributes=True)
