### Contributors: Lamonte Harris
### Description: Dependencies that are included in multiple files

from uuid import UUID

from fastapi import HTTPException
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import CookieParameters, SessionCookie
from starlette.templating import Jinja2Templates

from app.sessions.auth_session_data import AuthSessionData
from app.sessions.auth_verifier import AuthVerifier

### templates object that ties our template files to the template engine
templates = Jinja2Templates(directory="app/views")

### setup session + backend cookies
cookie_params = CookieParameters()

# + more cookies uses UUID
cookie = SessionCookie(
    cookie_name="cookie",
    identifier="auth_verifier",
    auto_error=False,
    secret_key="DONOTUSE", # create unique hash for this eventually
    cookie_params=cookie_params,
)

session = InMemoryBackend[UUID, AuthSessionData]()

verifier = AuthVerifier(
    identifier="auth_verifier",
    auto_error=False,  # off so it doesn't kill our application
    backend=session,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)