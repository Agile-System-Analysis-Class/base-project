from app.database.models import AttendanceModel, CoursesModel
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

    dates = pandas.date_range(start=start_date_parsed, end=finish_date_parsed).strftime("%m/%d/%Y")

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
