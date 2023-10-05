from database.models import ClientModel, CoursesModel, TeachingCoursesRegisteredModel, CoursesRegisteredModel


# this function filters through the database fields instead of using join data
# with existing data. Then we return an array of all the professors and the courses they're
# assigned to.
def filter_generated_data(accounts: list[ClientModel],
                          courses: list[CoursesModel],
                          course_data: list[TeachingCoursesRegisteredModel],
                          student_course_data: list[CoursesRegisteredModel]):
    students_list = []
    for stud in accounts:
        if stud.account_type != 3:
            continue
        students_list.append(stud)

    professor_data = []
    for prof in accounts:
        if prof.account_type != 2:
            continue

        prof_courses = []
        for c_data in course_data:
            if c_data.client_id == prof.id:
                prof_courses.append(c_data)

        # will store an array of this professors courses and it'll have a sub list of students for that course
        course_list = []

        # loop through professor course data so we can grab that professors courses and the students under that course
        for prof_course_data in prof_courses:
            cur_course = filter_course_by_id(prof_course_data.course_id, courses)
            if cur_course is None:
                continue
            students = filter_students_by_course_id(cur_course.id, students_list, student_course_data)

            course_list.append({
                "course": cur_course,
                "students": students
            })

        professor_data.append({
            "professor": prof,
            "courses": course_list
        })

    return professor_data

def filter_course_by_id(course_id: int, courses: list[CoursesModel]):
    for course in courses:
        if course.id == course_id:
            return course
    return None


def filter_students_by_course_id(course_id: int,
                                 students: list[ClientModel], course_data: list[CoursesRegisteredModel]):
    # loop through the course model data so we can grab the students from that course
    students_data = []
    for data in course_data:
        # ignore courses we don't want
        if data.course_id != course_id:
            continue
        student = filter_students_by_student_id(data.client_id, students)
        if student is not None:
            students_data.append(student)
    return students_data


def filter_students_by_student_id(student_id: int, students: list[ClientModel]):
    for student in students:
        if student.id == student_id:
            return student
    return None
