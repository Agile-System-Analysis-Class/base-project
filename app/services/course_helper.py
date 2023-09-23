# filter our dummy coursre data until we implement actual database models
def filter_courses(uid: int, course_data: list[dict], courses: list[dict], type: int):
    found = []
    for data in course_data:

        test_id = data.get("student_id", None)
        if type == 1:
            test_id = data.get("teacher_id", None)

        if test_id != uid:
            continue

        course_id = data.get("course_id", None)
        for course in courses:
            cid = course.get("id", None)
            if cid == course_id:
                found.append(course)
    return found
