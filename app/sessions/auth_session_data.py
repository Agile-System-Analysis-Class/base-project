from pydantic import BaseModel


class AuthSessionData(BaseModel):
    username: str
    isStudent: bool
