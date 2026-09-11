from pydantic import BaseModel, ConfigDict



# Filter for henting av data

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)
