from database.models import TeachingCoursesRegisteredModel
from database.engine import engine
from sqlmodel import Session, select

def find_all_teaching_courses():
    with Session(engine) as db:
        query = select(TeachingCoursesRegisteredModel)
        results = db.exec(query).all()
        return results