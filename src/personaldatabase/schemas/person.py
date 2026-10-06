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
    is_active: bool = True


# Skjema for å opprette ny person
class person_create(person_base):
    pass

# Skjema for å oppdatere person
class person_update(BaseModel):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    school: str | None = None
    last_signed_contract: date | None = None
    phone_number: str | None = None
    postbox: str | None = None
    street_name: str | None = None
    student_card_number: int | None = None
    status: bool | None = None
    birthdate: date | None = None
    picture: str | None = None
    gender: str | None = None

# Filter for henting av data
class person_response(person_base):
    id: int

    model_config = ConfigDict(from_attributes=True)
