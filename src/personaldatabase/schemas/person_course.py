from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class CourseMemberAdd(BaseModel):
    person_id: int
    course_date: date = Field(default_factory=date.today)


class CourseMemberResponse(BaseModel):
    person_id: int
    course_id: int
    course_date: date

    model_config = ConfigDict(from_attributes=True)


# Aliases for fleksibilitet og konsistens
CourseParticipantAdd = CourseMemberAdd
CourseParticipantResponse = CourseMemberResponse
