from pydantic import BaseModel, Field


class AuthSessionData(BaseModel):
    id: int = Field(default=0)
    username: str
    is_student: bool
