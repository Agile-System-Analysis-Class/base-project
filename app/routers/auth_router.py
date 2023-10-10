### Contributors: Lamonte Harris
### Description: These routes are used to transverse through the website, login/logout routes
### for it, professors and students using example generated data

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Request, Response, Depends, Form
from starlette.responses import HTMLResponse, RedirectResponse

from app.dependencies import cookie, verifier, templates, session
from app.domain.clients.clients_service import get_authenticated_user
from app.sessions.auth_session_data import AuthSessionData
from app.sessions.authenticate import Authenticate

router = APIRouter()

@router.get("/login", response_class=HTMLResponse, dependencies=[Depends(cookie)])
def login_page(request: Request, session_data: AuthSessionData = Depends(verifier)):
    """
    This route allows the user to login
    :param request:
    :param session_data:
    :return: Response
    """
    if session_data:
        return RedirectResponse("/")
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login", dependencies=[Depends(cookie)])
async def login_page(
    response: Response,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session_data: AuthSessionData = Depends(verifier)
):
    """
    This route allows the user to take a post request to
    set the login session if the credentials they passed were legit

    :param response:
    :param email:
    :param password:
    :param session_data:
    :return: JsonResponse
    """
    # check if user is already logged in
    if session_data:
        return {"status": True, "message": "already logged in"}

    account = get_authenticated_user(email, password)
    if account is not None:
        auth = Authenticate(response, session, cookie)
        await auth.session_create(account.id, account.email, account.firstname, account.account_type)
        return {"status": True, "message": "Logged in successfully!"}
    return {"status": False, "message": "Login failed, please try again!"}


@router.get('/logout', dependencies=[Depends(cookie)])
async def logout(
    response: Response,
    session_id: UUID = Depends(cookie),
    session_data: AuthSessionData = Depends(verifier)
):
    """
    This route allows the user to logout, clears any set sessions and redirects them to the index
    which would then send them to the login since no session data was found.

    :param response:
    :param session_id:
    :param session_data:
    :return: Response
    """
    if session_data:
        await session.delete(session_id)
        cookie.delete_from_response(response)
    return RedirectResponse("/login")