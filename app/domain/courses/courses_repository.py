import random
import string

from app.database.models import ClientModel, CoursesModel, CoursesRegisteredModel, TeachingCoursesRegisteredModel
from app.database.engine import engine
from sqlmodel import Session, select

def find_all_courses():
    with Session(engine) as db:
        query = select(CoursesModel)
        results = db.exec(query).all()
        return results


def find_professor_courses_by_client_id(cid: int):
    courses = []
    with Session(engine) as db:
        query = select(TeachingCoursesRegisteredModel, CoursesModel).join(CoursesModel
                    ).where(TeachingCoursesRegisteredModel.client_id == cid)

        results = db.exec(query)
        for (registered, course) in results:
            courses.append(course)
    return courses

def find_student_courses_by_client_id(cid: int):
    courses = []
    with Session(engine) as db:
        query = select(CoursesRegisteredModel, CoursesModel).join(CoursesModel
                    ).where(CoursesRegisteredModel.client_id == cid)

        results = db.exec(query)
        for (registered, course) in results:
            courses.append(course)
    return courses


def find_course(cid: int):
    with Session(engine) as db:
        query = select(CoursesModel).where(CoursesModel.id == cid)
        result = db.exec(query).one_or_none()
        return result

def find_course_students_by_id(cid: int):
    students = []
    with Session(engine) as db:
        query = select(CoursesRegisteredModel, ClientModel).join(ClientModel).where(CoursesRegisteredModel.course_id == cid)
        results = db.exec(query)
        for (course, client) in results:
            students.append(client)
    return students

def generate_and_store_course_access_code(cid: int):
    code = generate_random_string()
    course = find_course(cid)
    if course is not None:
        course.access_code = code
        save(course)
        return code
    return None


    # with Session(engine) as db:
def save(course: CoursesModel):
    with Session(engine) as db:
        db.add(course)
        db.commit()

def generate_random_string(length: int = 8):
    return ''.join(random.choices(string.ascii_letters, k=length))