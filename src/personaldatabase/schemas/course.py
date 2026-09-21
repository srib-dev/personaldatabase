from pydantic import BaseModel, ConfigDict


# Filter for henting av data

class course_response(BaseModel):
    id: int
    course_name: str
    course_provider: str

    model_config = ConfigDict(from_attributes=True)
