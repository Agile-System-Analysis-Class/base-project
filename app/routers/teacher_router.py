### Contributors: Lamonte Harris
### Description: These routes are used to transverse through the website, professor routes for
### viewing courses taught, viewing students registered, viewing attendance report data and, allowing
### the professor to set a access token for a course they taught.
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Request, Depends, Form
from starlette.responses import RedirectResponse

from app.debugger.datetime_helpers import create_datetime_hours_list, create_datetime_mins_list, verify_date, \
    create_course_begin_timestamp, convert_timestamp_to_form_begin_mins, convert_timestamp_to_form_begin_hours, \
    convert_timestamp_to_form_begin_day, convert_timestamp_to_form_start_end_date
from app.dependencies import cookie, verifier, templates
from app.domain.courses.courses_repository import find_course, generate_and_store_course_access_code, \
    find_course_students_by_id, debugger_save_course_start_data
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

    """registered students in the course"""
    students = find_course_students_by_id(cid)

    # date time helper functions
    form_mins = create_datetime_mins_list()
    form_hours = create_datetime_hours_list()

    # grab prefilled course begin hour/min/pm|am data
    debug_pm = convert_timestamp_to_form_begin_day(course.meeting_start_time)
    debug_course_min = convert_timestamp_to_form_begin_mins(course.meeting_start_time, form_mins)
    debug_course_hour = convert_timestamp_to_form_begin_hours(course.meeting_start_time)

    # parse start/end dates
    start_date_parsed = convert_timestamp_to_form_start_end_date(course.start_date)
    finish_date_parsed = convert_timestamp_to_form_start_end_date(course.finish_date)

    return templates.TemplateResponse("teacher/course.html", {
        "request": request,
        "course": course,
        "students": students,
        "form": {
            "mins": form_mins,
            "hours": form_hours,
            "start_date": start_date_parsed,
            "finish_date": finish_date_parsed,
            "selected_pm": debug_pm,
            "selected_min": debug_course_min,
            "selected_hour": debug_course_hour,
        }
    })


@router.post('/teacher/course_set_data/{cid}', dependencies=[Depends(cookie)])
async def teacher_course_set_data(
    cid: int,
    start_date: Annotated[str, Form()],
    end_date: Annotated[str, Form()],
    set_day: Annotated[str, Form()],
    set_min: Annotated[str, Form()],
    set_hour: Annotated[str, Form()],
    sess: AuthSessionData = Depends(verifier)
):
    """
    This route handles setting the course start data using the debugger for testing
    the attendance functionality

    :param start_date:
    :param end_date:
    :param set_hour:
    :param set_min:
    :param set_day:
    :param cid:
    :param request:
    :param sess:
    :return: Response
    """
    if not sess:
        return {"status": False, "message": "not authenticated"}

    course = find_course(cid)
    if course is None:
        return {"status": False, "message": "You don't teach this course"}

    # date time helper functions
    form_mins = create_datetime_mins_list(as_string=True)
    form_hours = create_datetime_hours_list(as_string=True)

    # verify the date time values are valid for when the course hour starts
    if set_min not in form_mins:
        return {"status": False, "message": "Form min isn't formatted correctly"}
    if set_hour not in form_hours:
        return {"status": False, "message": "Form hour isn't formatted correctly"}
    if set_day not in ["am", "pm"]:
        return {"status": False, "message": "Form day isn't formatted correctly"}

    # verify the start and end dates are valid
    current_start_date = verify_date(start_date)
    current_end_date = verify_date(end_date)
    if not current_start_date:
        return {"status": False, "message": "Course start date is formatted incorrectly"}
    if not current_end_date:
        return {"status": False, "message": "Course end date is formatted incorrectly"}

    # get generated course begin timestamp based off 2nd day created in code 1970/Jan 2nd
    begin_course_date = create_course_begin_timestamp(set_hour, set_min, set_day)

    # save course data
    debugger_save_course_start_data(course, current_start_date, current_end_date, begin_course_date)

    return {"status": True, "message": "Made it to the end!"}

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