from uuid import uuid4

from fastapi import Response
from fastapi_sessions.backends import SessionBackend
from fastapi_sessions.frontends.implementations import SessionCookie

from sessions.auth_session_data import AuthSessionData


class Authenticate:
    response: Response
    backend: SessionBackend
    cookie: SessionCookie

    def __init__(self, response: Response, backend: SessionBackend, cookie: SessionCookie):
        self.cookie = cookie
        self.backend = backend
        self.response = response

    async def session_create(self, _id: int, email: str, username: str, account_type: int):
        uniq = uuid4()
        data = AuthSessionData(id=_id, username=username, email=email, account_type=account_type)

        await self.backend.create(uniq, data)
        self.cookie.attach_to_response(self.response, uniq)

        return username
