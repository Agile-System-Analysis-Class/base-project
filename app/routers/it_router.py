### Contributors: Lamonte Harris
### Description: These routes are used to transverse through the website, administrator routes

from fastapi import APIRouter, Request, Depends
from starlette.responses import HTMLResponse, RedirectResponse

from app.database.helpers import setup_database_data
from app.dependencies import templates, cookie, verifier
from app.domain.clients.clients_repository import find_by_session
from app.domain.root.root_repository import generate_demo_data
from app.sessions.auth_session_data import AuthSessionData

router = APIRouter()

@router.get('/env_setup', response_class=HTMLResponse)
async def db_create(request: Request):
    """
    Sets up the db tables & root account

    :param request:
    :return: Response
    """
    setup_database_data()
    return templates.TemplateResponse("setup_complete.html", {
        "request": request,
    })


@router.get("/generate_data", dependencies=[Depends(cookie)])
def root_generate_data(sess: AuthSessionData = Depends(verifier)):
    if not sess:
        return RedirectResponse("/login")

    account = find_by_session(sess)
    if account is None or account.account_type != 1:
        return {"status": False, "message": "Invalid user account"}

    generate_demo_data()

    return {"status": True, "message": "Website data generated"}