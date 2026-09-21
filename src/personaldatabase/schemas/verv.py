from pydantic import BaseModel, ConfigDict


# Filter for henting av data

class verv_response(BaseModel):
    id: int
    verv_name: str
    role: str

    model_config = ConfigDict(from_attributes=True)
