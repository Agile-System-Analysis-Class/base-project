from app.database.models import CoursesRegisteredModel
from app.database.engine import engine
from sqlmodel import Session, select

def find_all_student_courses():
    with Session(engine) as db:
        query = select(CoursesRegisteredModel)
        results = db.exec(query).all()
        return results