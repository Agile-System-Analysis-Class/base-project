def get_user(uid: int, students: list[dict]):
    for student in students:
        sid = student.get("id")
        if sid == uid:
            return student
    return None