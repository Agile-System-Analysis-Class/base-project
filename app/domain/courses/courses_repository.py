from database.models import ClientModel, CoursesModel, CoursesRegisteredModel, TeachingCoursesRegisteredModel
from database.engine import engine
from domain.clients.clients_repository import create_password
from sqlmodel import Session, select

def find_course_by_client_id(id: int):
    with Session(engine) as db:
        # delete all users and courses that aren't root
        query = select(ClientModel).where(CoursesRegisteredModel.client_id == id)