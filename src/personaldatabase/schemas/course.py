from pydantic import BaseModel, ConfigDict


# Skjema for å opprette nytt kurs
class CourseCreate(BaseModel):
    course_name: str
    course_provider: str


# Filter for henting av data
class CourseResponse(BaseModel):
    id: int
    course_name: str
    course_provider: str

    model_config = ConfigDict(from_attributes=True)


# Bakoverkompatibilitet
course_response = CourseResponse
course_create = CourseCreate