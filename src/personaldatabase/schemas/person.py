from datetime import date

from pydantic import BaseModel, ConfigDict


# Filter for henting av data

class person_response(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    school: str
    last_signed_contract: date
    phone_number: str
    postbox: str
    street_name: str
    student_card_number: int
    status: bool
    birthdate: date
    picture: str
    gender: str

    model_config = ConfigDict(from_attributes=True)
