from datetime import date

from pydantic import BaseModel, ConfigDict


# Filter for henting av data

class person_response(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    school: str | None
    last_signed_contract: date | None
    phone_number: str | None
    postbox: str | None
    street_name: str | None
    student_card_number: str
    status: str | None
    birthdate: date
    picture: str | None
    gender: str | None

    model_config = ConfigDict(from_attributes=True)
