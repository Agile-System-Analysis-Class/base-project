### Contributors: Lamonte Harris
### Description: These routes are used to transverse through the website, dashboard routes allowing the admin to generate,
### example data, professor's to view their registered for teaching courses and students to view their current courses.

from fastapi import APIRouter, Request, Depends
from starlette.responses import HTMLResponse, RedirectResponse

from app.dependencies import cookie, verifier, templates
from app.domain.clients.clients_repository import find_by_session
from app.helpers.dashboard_helper import display_root_dashboard, display_professor_dashboard, display_student_dashboard
from app.sessions.auth_session_data import AuthSessionData

router = APIRouter()

@router.get("/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
def home_page(request: Request, sess: AuthSessionData = Depends(verifier)):
    """
    Switch between the according dashboard based on the type of account logged in
    showing either the IT demo generation routes, professor courses registered for teaching or
    the students courses they are registered to for attending.

    :param request:
    :param sess:
    :return: Response
    """
    if not sess:
        return RedirectResponse("/login")

    # check if the user data exists else, show an account error template
    account = find_by_session(sess)
    if account is None:
        return templates.TemplateResponse("account_error.html", {
            "request": request, "msg": "Account not found"})

    # setup variables for later usage
    temp: str
    context = {"request": request}

    # check account type to display the correct dashboard
    match account.account_type:
        case 1:
            temp = "root"
            context = display_root_dashboard(request, account)
        case 2:
            temp = "teacher"
            context = display_professor_dashboard(request, account)
        case 3:
            temp = "student"
            context = display_student_dashboard(request, account)
        case _:
            temp = "student"

    return templates.TemplateResponse(f"dashboard/{temp}.html", context)