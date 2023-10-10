### Contributors: Lamonte Harris
### Description: Teaching Courses Registered repository file used to grab data from the database based on the criteria we pass
### to the functions

from app.database.models import TeachingCoursesRegisteredModel
from app.database.engine import engine
from sqlmodel import Session, select

def find_all_teaching_courses():
    """
    Find all courses connecting data that are being taught, used for data generation

    :return: List[TeachingCoursesRegisteredModel]
    """
    with Session(engine) as db:
        query = select(TeachingCoursesRegisteredModel)
        results = db.exec(query).all()
        return results