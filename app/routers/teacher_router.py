### Contributors: Lamonte Harris
### Description: These routes are used to transverse through the website, professor routes for
### viewing courses taught, viewing students registered, viewing attendance report data and, allowing
### the professor to set a access token for a course they taught.

from fastapi import APIRouter, Request, Depends
from starlette.responses import RedirectResponse

from app.dependencies import cookie, verifier, templates
from app.domain.courses.courses_repository import find_course, generate_and_store_course_access_code, \
    find_course_students_by_id
from app.sessions.auth_session_data import AuthSessionData

router = APIRouter()

@router.get('/teacher/course/{cid}', dependencies=[Depends(cookie)])
async def teacher_course(
    cid: int,
    request: Request,
    sess: AuthSessionData = Depends(verifier)
):
    """
    This route lists all the courses this professor teaches

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

    students = find_course_students_by_id(cid)

    return templates.TemplateResponse("teacher/course.html", {
        "request": request,
        "course": course,
        "students": students
    })

@router.get('/teacher/course/{cid}/access_code', dependencies=[Depends(cookie)])
async def teacher_access_code(
    cid: int,
    request: Request,
    sess: AuthSessionData = Depends(verifier)
):
    """
    This route shows the access code generation form and the currently set access token if one
    is set.

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

    return templates.TemplateResponse("teacher/generate_access_code.html", {
        "request": request,
        "course": course,
    })


@router.post('/teacher/course/{cid}/access_code', dependencies=[Depends(cookie)])
async def teacher_access_code(
    cid: int,
    sess: AuthSessionData = Depends(verifier)
):
    """
    This route handles the access post data when trying to regenerate a new access token

    :param cid:
    :param sess:
    :return: JsonResponse
    """
    status = True
    message: str

    if not sess:
        return {"status": status, "message": "not authenticated"}

    course = find_course(cid)
    if course is None:
        return {"status": status, "message": "You don't teach this course"}

    # set a new token in the database
    code = generate_and_store_course_access_code(cid)
    if code is not None:
        message = code
    else:
        message = "There was a problem generating access code for this course"
        status = False
    return {"status": status, "message": message}