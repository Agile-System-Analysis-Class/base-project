from pydantic import BaseModel, Field


class AuthSessionData(BaseModel):
    id: int = Field(default=0)
    email: str
    username: str
    account_type: int
