from app.database.models import CoursesModel
from app.domain.attendance.attendance_repository import find_attendance_by_course_and_student_id
from app.domain.clients.clients_repository import find_account_by_id
from app.domain.courses.courses_service import get_course_dates, get_course_dates_before_or_today


def get_student_attendance_dates(course: CoursesModel, student_id: int):

    attendance_dates = find_attendance_by_course_and_student_id(course.id, student_id)

    dates = []
    for date in attendance_dates:
        dates.append(date.date_marked_present)
    return dates

def get_student_attendance_dates_in_course(student_id: int, course: CoursesModel, course_dates: list):
    actual = []
    student_dates = get_student_attendance_dates(course, student_id)
    for date in student_dates:
        if date in course_dates:
            actual.append(date)
    return actual


def get_results(students: list[str], course: CoursesModel):
    """
    This function grabs the student attendance for this course if the course has started
    :param students:
    :param course:
    :return:
    """
    results = []

    course_dates = get_course_dates(course)
    course_dates_so_far = get_course_dates_before_or_today(course)
    print(course_dates_so_far)

    # course hasn't started yet
    if len(course_dates_so_far) <= 0:
        return None

    # try getting attendance information for all students
    for student_id in students:
        student = find_account_by_id(int(student_id))
        if student is None:
            continue

        # grab attendance data for student & the same data excluding days that hasn't happened yet
        dates_so_far = get_student_attendance_dates_in_course(int(student_id), course, course_dates_so_far)

        results.append({
            "student": student.to_json(),
            "attendance": f"{len(dates_so_far)} / {len(course_dates_so_far)} ({len(course_dates)})",
            "attendance_percent": f"{'%.2f' % ((len(dates_so_far) / len(course_dates_so_far)) * 100)}%",
        })

    return results