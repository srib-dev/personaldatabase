from pydantic import BaseModel, ConfigDict



# Filter for henting av data

class user_response(BaseModel):
    id: int
    verv_id: int
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)
