### Contributors: Lamonte Harris
### Description: These routes are used to transverse through the website, administrator routes
import json
from typing import Annotated

from fastapi import APIRouter, Request, Depends, Form
from starlette.responses import HTMLResponse, RedirectResponse

from app.dependencies import templates, cookie, verifier
from app.domain.clients.clients_repository import find_account, find_all_student_accounts
from app.domain.root.root_report_center_service import get_student_attendance_reports_by_ids
from app.sessions.auth_session_data import AuthSessionData

router = APIRouter()

@router.get("/report-center", response_class=HTMLResponse, dependencies=[Depends(cookie)])
def report_center(request: Request, sess: AuthSessionData = Depends(verifier)):
    """
    Switch between the according dashboard based on the type of account logged in
    showing either the IT demo generation routes, professor courses registered for teaching or
    the students courses they are registered to for attending.

    :param request:
    :param sess:
    :return: Response
    # """
    # if not sess:
    #     return RedirectResponse("/login")
    #
    # client = find_account(sess.email)
    client = find_account("root")
    if client is None:
        return RedirectResponse("/login")

    # # only a root/staff account route
    # if client.account_type != 1:
    #     return RedirectResponse("/")

    students = find_all_student_accounts()

    return templates.TemplateResponse("staff/report_center.html", {
        "request": request,
        "is_root": client.account_type == 1,
        "students": students,
    })

@router.post('/report-center/results', dependencies=[Depends(cookie)])
async def report_center_results(
    student_ids: Annotated[str, Form()],
    sess: AuthSessionData = Depends(verifier)
):
    """
    This route displays the attendance results for all students when requested

    :param student_ids:
    :param sess:
    :return: Response
    """
    # if not sess:
    #     return {"status": False, "message": "not authenticated"}

    try:
        ids = json.loads(student_ids)
        results = get_student_attendance_reports_by_ids(ids)
        return {"status": True, "data": results}
        # if results is None:
        #     return {"status": False, "message": "This course hasn't started yet. No attendance reports to show"}
        # else:
    except ValueError:
        return {"status": False, "message": "error"}