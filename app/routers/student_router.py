### Contributors: Lamonte Harris
### Description: These routes are used to transverse through the website, student routes used to
### view the current students registered courses, view the current students attendance and allows a student
### to set the current time, so they can test attending a course as if that day was set using the access token generated
### for that course.

from fastapi import APIRouter, Request, Depends
from starlette.responses import RedirectResponse

from app.dependencies import cookie, verifier, templates
from app.domain.courses.courses_repository import find_course
from app.sessions.auth_session_data import AuthSessionData

router = APIRouter()

@router.get('/student/course/{cid}', dependencies=[Depends(cookie)])
async def student_course(
    cid: int,
    request: Request,
    sess: AuthSessionData = Depends(verifier)
):
    """
    SHow the students current course if they are registered to it

    :param cid:
    :param request:
    :param sess:
    :return: Response
    """
    if not sess:
        return RedirectResponse("/login")

    course = find_course(cid)
    if course is None:
        return RedirectResponse("/login")

    return templates.TemplateResponse("student/course.html", {
        "request": request,
        "course": course,
    })


@router.get('/student/course/{cid}/checkin', dependencies=[Depends(cookie)])
async def student_course_checkin(
    cid: int,
    request: Request,
    sess: AuthSessionData = Depends(verifier)
):
    """
    Course that lets the student attempt to check in to a course that has started

    :param cid:
    :param request:
    :param sess:
    :return: Response
    """
    if not sess:
        return RedirectResponse("/login")

    course = find_course(cid)
    if course is None:
        return RedirectResponse("/login")

    # todo: when we add actual data we need to tell the js when the class started when the page loads
    return templates.TemplateResponse("student/course_checkin.html", {
        "request": request,
        "course": course,
    })