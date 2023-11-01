from sqlmodel import Session, select

from app.database.engine import engine
from app.database.models import AttendanceModel, ClientModel, CoursesModel


def find_attendance_by_course_and_student_id(course_id: int, student_id: int):
    """
    Find attendance data for student and course id set

    :param course_id:
    :param student_id:
    :return: list[AttendanceModel]
    """

    attendance = []
    with Session(engine) as db:
        query = select(AttendanceModel).where(AttendanceModel.client_id == student_id).where(AttendanceModel.course_id == course_id)
        results = db.exec(query)
        for att in results:
            attendance.append(att)
    return attendance


