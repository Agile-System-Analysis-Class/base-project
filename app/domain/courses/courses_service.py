### Contributors: Lamonte Harris
### Description: courses services that helps us bring together common functionality for courses

from datetime import datetime

import pytz

from app.database.models import AttendanceModel, CoursesModel, ClientModel
from app.debugger.datetime_helpers import convert_timestamp_to_form_start_end_date
import pandas

from app.domain.attendance.attendance_repository import find_attendance_by_course_and_student_id


def list_course_date_range(start_date: int, finish_date: int):
    """takes the start/end dates and creates a list range of dates we'll use to display to the user
    for their attendance table"""
    dates = []

    if start_date == 0 or finish_date == 0:
        return dates

    start_date_parsed = convert_timestamp_to_form_start_end_date(start_date, return_none=True)
    finish_date_parsed = convert_timestamp_to_form_start_end_date(finish_date, return_none=True)

    matches = pandas.date_range(start=start_date_parsed, end=finish_date_parsed).strftime("%m/%d/%Y")
    for match in matches:
        dates.append(match)

    return dates


def list_course_data_with_attendance_check(dates: list, attendance: list[AttendanceModel]):
    """
    Takes course dates list and current students attendance data and sets if the student attended
    one of the course dates used in the student course table

    :param dates:
    :param attendance:
    :return:
    """
    attend_dates = []
    for attend in attendance:
        attend_dates.append(attend.date_marked_present)

    dates_list = []
    for date in dates:
        attended = False
        if date in attend_dates:
            attended = True
        dates_list.append({"date": date, "attended": attended})

    return dates_list


def get_course_dates(course: CoursesModel):
    """Get a list of dates for the current course"""
    return list_course_date_range(course.start_date, course.finish_date)

def get_course_dates_before_or_today(course: CoursesModel):
    """Get a list of the actual course dates that has happened, exclude those that hasn't"""
    actual = []
    today = datetime.today()
    course_dates = get_course_dates(course)
    for date in course_dates:
        date_parts = date.split("/", 3)

        # only want 3 part dates, else something went wrong in the formatting
        if len(date_parts) != 3:
            continue

        day = int(date_parts[1])
        month = int(date_parts[0])
        year = int(date_parts[2])

        """we make sure all dates for the course are only the dates that happened so far in real
        time, excluding days that hasn't actually happened yet."""
        if year > today.year:
            continue
        elif year == today.year and month > today.month:
            continue
        elif year == today.year and month == today.month and day > today.day:
            continue
        else:
            actual.append(date)
    return actual


def get_student_attendance_data(course: CoursesModel, student_id: int):
    """
    This function grabs the course start/finish data and student attendance data
    and creates a list of dates that show which days the student attended

    :param course:
    :param student_id:
    :return:
    """
    course_dates = list_course_date_range(course.start_date, course.finish_date)
    if course_dates is None:
        return []

    attendance_data = find_attendance_by_course_and_student_id(course.id, student_id)
    attendance_dates = list_course_data_with_attendance_check(course_dates, attendance_data)

    return attendance_dates


def course_has_attend_date(today: int, course: CoursesModel):
    """USed to check if the current course has actual attend date"""
    dt = convert_timestamp_to_form_start_end_date(today)

    course_dates = list_course_date_range(course.start_date, course.finish_date)
    if course_dates is None:
        return False

    if dt not in course_dates:
        return False
    return True


def missed_course_attend_time(today: int, course: CoursesModel):
    """check if the course check in time already ended in CST timezone"""
    now = datetime.fromtimestamp(today)
    if today == 0:
        now = datetime.now(pytz.timezone('US/Central'))

    course_begin_time = datetime.fromtimestamp(course.meeting_start_time)

    # course time must be same hour
    if now.hour != course_begin_time.hour:
        return True

    # course minute must be within the start window
    start_window_mins = 10

    """more readable than the version pycharm recommended"""
    if now.minute >= course_begin_time.minute and now.minute <= course_begin_time.minute + start_window_mins:
        return False
    return True


def student_course_checked_in(today: int, course: CoursesModel, client: ClientModel):
    """Check if the student already checked into this course at the correct time"""
    dt = convert_timestamp_to_form_start_end_date(today)

    # check if the course is setup first, early exit
    course_dates = list_course_date_range(course.start_date, course.finish_date)
    if course_dates is None:
        return False

    # grab attendance data for this student and see if they already checked in
    attendance_data = find_attendance_by_course_and_student_id(course.id, client.id)

    attend_dates = []
    for attend in attendance_data:
        attend_dates.append(attend.date_marked_present)

    if dt not in attend_dates:
        return False

    return True


def student_attend_show_text_or_link(client: ClientModel, course: CoursesModel):
    """Used to show the verify button to check into the course if available/can"""
    can_verify = True
    can_verify_text = "Check into course"

    if not course_has_attend_date(client.current_time_override, course):
        can_verify = False
        can_verify_text = ""
    elif student_course_checked_in(client.current_time_override, course, client):
        can_verify = False
        can_verify_text = "Already Checked In"
    elif missed_course_attend_time(client.current_time_override, course):
        can_verify = False
        can_verify_text = "Missed check in time"

    return {"can_attend": can_verify, "text": can_verify_text}