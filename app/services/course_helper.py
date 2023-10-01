# filter our dummy course data until we implement actual database models
from database.models import ClientModel


def filter_courses(uid: int, course_data: list[dict], courses: list[dict], ctype: int):
    found = []
    for data in course_data:

        test_id = data.get("student_id", None)
        if ctype == 1:
            test_id = data.get("teacher_id", None)

        if test_id != uid:
            continue

        course_id = data.get("course_id", None)
        for course in courses:
            cid = course.get("id", None)
            if cid == course_id:
                found.append(course)
    return found


def get_course(cid: int, courses: list[dict]):
    for course in courses:
        if cid == course.get("id", None):
            return course
    return None

def course_exists(current: dict, courses: list[dict]):
    for course in courses:
        if current.get("id") == course.get("id"):
            return True
    return False

def course_students(current: dict, cdata: list[dict], students: list[dict]):
    c_id = current.get("id")
    if not c_id:
        return None

    found = []

    for data in cdata:
        cid = data.get("course_id")
        if cid != c_id:
            continue
        student_id = data.get("student_id")
        if student_id:
            for student in students:
                sid = student.get("id")
                if sid == student_id:
                    found.append(student)

    return found

# def account_dashboard(account: ClientModel)