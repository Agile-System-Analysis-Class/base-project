### Contributors: Lamonte Harris
### Description: These routes are used to transverse through the website, student routes used to
### view the current students registered courses, view the current students attendance and allows a student
### to set the current time, so they can test attending a course as if that day was set using the access token generated
### for that course.
from typing import Annotated

from fastapi import APIRouter, Request, Depends, Form
from starlette.responses import RedirectResponse

from app.database.helpers import save
from app.database.models import AttendanceModel
from app.debugger.datetime_helpers import create_datetime_mins_list, create_datetime_hours_list, verify_date, \
    create_student_timestamp, convert_timestamp_to_form_begin_day, convert_timestamp_to_form_begin_mins, \
    convert_timestamp_to_form_begin_hours, convert_timestamp_to_form_start_end_date, create_student_override_date
from app.dependencies import cookie, verifier, templates
from app.domain.clients.clients_repository import find_account
from app.domain.courses.courses_repository import find_course
from app.domain.courses.courses_service import list_course_date_range, get_student_attendance_data, \
    course_has_attend_date, student_course_checked_in, missed_course_attend_time
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

    client = find_account(sess.email)
    if client is None:
        return RedirectResponse("/login")

    course = find_course(cid)
    if course is None:
        return RedirectResponse("/login")

    # date time helper functions
    form_mins = create_datetime_mins_list()
    form_hours = create_datetime_hours_list()

    # grab prefilled course begin hour/min/pm|am data
    debug_pm = convert_timestamp_to_form_begin_day(client.current_time_override)
    debug_course_min = convert_timestamp_to_form_begin_mins(client.current_time_override, form_mins)
    debug_course_hour = convert_timestamp_to_form_begin_hours(client.current_time_override)

    # default form field overrides
    if client.current_time_override == 0:
        debug_pm = "am"
        debug_course_min = -1
        debug_course_hour = -1

    # parse current time, using override student data if exists
    current_date_parsed = convert_timestamp_to_form_start_end_date(client.current_time_override)

    # parsed current time or overridden time we set in a readable sense converted to local timezone (central)
    current_date = create_student_override_date(client.current_time_override)

    # parse course dates along w/ student attendance information
    course_dates = get_student_attendance_data(course, client.id)

    return templates.TemplateResponse("student/course.html", {
        "date": current_date,
        "request": request,
        "course": course,
        "course_dates": course_dates,
        "form": {
            "mins": form_mins,
            "hours": form_hours,
            "current_date": current_date_parsed,
            "selected_pm": debug_pm,
            "selected_min": debug_course_min,
            "selected_hour": debug_course_hour,
        }
    })


@router.get('/student/course/{cid}/attendance', dependencies=[Depends(cookie)])
async def student_course_attendance(
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

    client = find_account(sess.email)
    if client is None:
        return RedirectResponse("/login")

    course = find_course(cid)
    if course is None:
        return RedirectResponse("/login")

    # make sure course date actually exists before checking if they can check in
    course_attend_day_exists = course_has_attend_date(client.current_time_override, course)
    if not course_attend_day_exists:
        return RedirectResponse(f"/student/course/{course.id}")

    is_attended = student_course_checked_in(client.current_time_override, course, client)
    if is_attended:
        return RedirectResponse(f"/student/course/{course.id}")

    # display different template if they missed attendance window
    if missed_course_attend_time(client.current_time_override, course):
        return templates.TemplateResponse("student/course_attendance_missed.html", {
            "request": request,
            "course": course,
        })

    return templates.TemplateResponse("student/course_attendance.html", {
        "request": request,
        "course": course,
        "is_attended": is_attended
    })


@router.post('/student/course/{cid}/attendance', dependencies=[Depends(cookie)])
async def student_course_attendance(
    cid: int,
    access_code: Annotated[str, Form()],
    sess: AuthSessionData = Depends(verifier)
):
    """
    Course that lets the student attempt to check in to a course that has started

    :param cid:
    :param sess:
    :param access_code:
    :return: Response
    """
    if not sess:
        return {"status": False, "message": "not authenticated"}

    if sess.account_type != 3:
        return {"status": False, "message": "invalid student account"}

    client = find_account(sess.email)
    if client is None:
        return {"status": False, "message": "invalid student account"}

    course = find_course(cid)
    if course is None:
        return {"status": False, "message": "invalid course id for this account"}

    if access_code != course.access_code:
        return {"status": False, "message": "invalid course access code"}

    # make sure course date actually exists before checking if they can check in
    course_attend_day_exists = course_has_attend_date(client.current_time_override, course)
    if not course_attend_day_exists:
        return {"status": False, "message": "Course attend date doesn't exist"}

    is_attended = student_course_checked_in(client.current_time_override, course, client)
    if is_attended:
        return {"status": False, "message": "student is already checked into this course for the day"}

    # parse current time, using override student data if exists & create a new attendance entry for today
    current_date_parsed = convert_timestamp_to_form_start_end_date(client.current_time_override)
    attendance = AttendanceModel(client_id=client.id, course_id=course.id, date_marked_present=current_date_parsed)
    save(attendance)

    return {"status": True, "message": "student self checked into this course for the date"}

@router.post('/student/set_current_time', dependencies=[Depends(cookie)])
async def student_set_current_time(
    current_date: Annotated[str, Form()],
    set_day: Annotated[str, Form()],
    set_min: Annotated[str, Form()],
    set_hour: Annotated[str, Form()],
    sess: AuthSessionData = Depends(verifier)
):
    """
    This route handles setting the course start data using the debugger for testing
    the attendance functionality

    :param current_date:
    :param set_hour:
    :param set_min:
    :param set_day:
    :param sess:
    :return: Response
    """
    if not sess:
        return {"status": False, "message": "not authenticated"}

    if sess.account_type != 3:
        return {"status": False, "message": "invalid student account"}

    client = find_account(sess.email)
    if client is None:
        return {"status": False, "message": "invalid student account"}

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
    current_date = verify_date(current_date)
    if not current_date:
        return {"status": False, "message": "Course start date is formatted incorrectly"}

    # get generated course begin timestamp based off 2nd day created in code 1970/Jan 2nd
    current_datetime = create_student_timestamp(current_date, set_hour, set_min, set_day)
    client.current_time_override = current_datetime

    # save course data
    save(client)

    return {"status": True, "message": "Current time override set"}


@router.post('/student/clear_current_time', dependencies=[Depends(cookie)])
async def student_clear_current_time(
    sess: AuthSessionData = Depends(verifier)
):
    """
    This route handles setting the course start data using the debugger for testing
    the attendance functionality

    :param sess:
    :return: Response
    """
    if not sess:
        return {"status": False, "message": "not authenticated"}

    if sess.account_type != 3:
        return {"status": False, "message": "invalid student account"}

    client = find_account(sess.email)
    if client is None:
        return {"status": False, "message": "invalid student account"}

    client.current_time_override = 0

    # save course data
    save(client)

    return {"status": True, "message": "Current time override reset"}