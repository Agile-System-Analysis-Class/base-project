### Contributors: Lamonte Harris
### Description: Functions we use to help organize the dashboard routes a bit cleaner

from app.database.models import ClientModel
from app.domain.clients.clients_repository import find_all_accounts
from app.domain.courses.courses_repository import find_professor_courses_by_client_id, find_student_courses_by_client_id
from app.domain.courses.courses_repository import find_all_courses
from app.domain.courses.teaching_courses_registered_repository import find_all_teaching_courses
from app.domain.courses.courses_registered_repository import find_all_student_courses
from app.domain.root.root_dashboard_service import filter_generated_data
from fastapi import Request


def display_root_dashboard(request: Request, acct: ClientModel):
    """
    This method shows generated data that was created in the database

    :param request:
    :param acct:
    :return:
    """
    accounts = find_all_accounts()
    courses = find_all_courses()
    professor_course_data = find_all_teaching_courses()
    student_course_data = find_all_student_courses()

    data = filter_generated_data(accounts, courses, professor_course_data, student_course_data)
    # print(data)

    return {"request": request, "data": data}

def display_professor_dashboard(request: Request, acc: ClientModel):
    """
    This shows all the professors courses they are teaching this semester

    :param request:
    :param acc:
    :return:
    """
    courses = find_professor_courses_by_client_id(acc.id)
    return {"request": request, "courses": courses}

def display_student_dashboard(request: Request, acc: ClientModel):
    """
    This shows all the students courses they are attending this semester

    :param request:
    :param acc:
    :return:
    """
    courses = find_student_courses_by_client_id(acc.id)
    return {"request": request, "courses": courses}