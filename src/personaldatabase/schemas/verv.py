from pydantic import BaseModel, ConfigDict


# Skjema for å opprette nytt verv
class VervCreate(BaseModel):
    verv_name: str
    role: str


# Filter for henting av data
class VervResponse(BaseModel):
    id: int
    verv_name: str
    role: str

    model_config = ConfigDict(from_attributes=True)


# Bakoverkompatibilitet
verv_response = VervResponse
verv_create = VervCreate
