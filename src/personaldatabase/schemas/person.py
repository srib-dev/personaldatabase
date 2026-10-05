from datetime import date

from pydantic import BaseModel, ConfigDict


# Filter for henting av data

class person_base(BaseModel):
    email: str
    first_name: str
    last_name: str
    school: str
    last_signed_contract: date
    phone_number: str
    postbox: str
    street_name: str
    student_card_number: int
    status: bool = True
    birthdate: date
    picture: str
    gender: str


# Skjema for å opprette ny person
class person_create(person_base):
    pass


# Filter for henting av data
class person_response(person_base):
    id: int

    model_config = ConfigDict(from_attributes=True)
