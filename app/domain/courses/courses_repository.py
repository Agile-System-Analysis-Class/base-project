### Contributors: Lamonte Harris
### Description: Courses repository file used to grab data from the database based on the criteria we pass
### to the functions

import random
import string

from app.database.helpers import save
from app.database.models import ClientModel, CoursesModel, CoursesRegisteredModel, TeachingCoursesRegisteredModel
from app.database.engine import engine
from sqlmodel import Session, select

def find_all_courses():
    """
    Grabs all courses from the db if they exist

    :return: list[CoursesModel]
    """
    with Session(engine) as db:
        query = select(CoursesModel)
        results = db.exec(query).all()
        return results


def find_professor_courses_by_client_id(cid: int):
    """
    Find all professor's courses by the client id (professor id) passed.

    :param cid:
    :return:  list[CoursesModel]
    """
    courses = []
    with Session(engine) as db:
        query = select(TeachingCoursesRegisteredModel, CoursesModel).join(CoursesModel
                    ).where(TeachingCoursesRegisteredModel.client_id == cid)

        results = db.exec(query)
        for (registered, course) in results:
            courses.append(course)
    return courses


def find_student_courses_by_client_id(cid: int):
    """
    Find all students courses by the client id (students id)

    :param cid:
    :return: list[CoursesModel]
    """
    courses = []
    with Session(engine) as db:
        query = select(CoursesRegisteredModel, CoursesModel).join(CoursesModel
                    ).where(CoursesRegisteredModel.client_id == cid)

        results = db.exec(query)
        for (registered, course) in results:
            courses.append(course)
    return courses


def find_course(cid: int):
    """
    Find course by id if it exists

    :param cid:
    :return: CoursesModel
    """
    with Session(engine) as db:
        query = select(CoursesModel).where(CoursesModel.id == cid)
        result = db.exec(query).one_or_none()
        return result


def find_course_students_by_id(cid: int):
    """
    Find all students in a course by the course id

    :param cid:
    :return: list[ClientModel]
    """
    students = []
    with Session(engine) as db:
        query = select(CoursesRegisteredModel, ClientModel).join(ClientModel).where(CoursesRegisteredModel.course_id == cid)
        results = db.exec(query)
        for (course, client) in results:
            students.append(client)
    return students


def generate_and_store_course_access_code(cid: int):
    """
    Generate a random access code and update that courses access code by the course id if it exists

    :param cid:
    :return: str|None
    """
    code = generate_random_string()
    course = find_course(cid)
    if course is not None:
        course.access_code = code
        save(course)
        return code
    return None


def generate_random_string(length: int = 8):
    """
    Generates a random string using python standard library

    :param length:
    :return: str
    """
    return ''.join(random.choices(string.ascii_letters, k=length))


def debugger_save_course_start_data(course: CoursesModel, start_date: int, end_date: int, begin_hour: int):
    """
    Stores the debugger data we set for this course used to test the attendance data

    :param course:
    :param start_date:
    :param end_date:
    :param begin_hour:
    :return:
    """
    course.start_date = start_date
    course.finish_date = end_date
    course.meeting_start_time = begin_hour
    save(course)