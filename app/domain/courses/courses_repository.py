from database.models import ClientModel, CoursesModel, CoursesRegisteredModel, TeachingCoursesRegisteredModel
from database.engine import engine
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