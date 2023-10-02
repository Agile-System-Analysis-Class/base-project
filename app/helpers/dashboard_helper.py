from database.models import ClientModel
from domain.courses.courses_repository import find_professor_courses_by_client_id, find_student_courses_by_client_id
from fastapi import Request

def display_root_dashboard(request: Request, acct: ClientModel):
    return {"request": request}

def display_professor_dashboard(request: Request, acc: ClientModel):
    courses = find_professor_courses_by_client_id(acc.id)
    return {"request": request, "courses": courses}

def display_student_dashboard(request: Request, acc: ClientModel):
    courses = find_student_courses_by_client_id(acc.id)
    return {"request": request, "courses": courses}