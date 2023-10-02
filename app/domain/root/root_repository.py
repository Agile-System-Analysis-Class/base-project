from database.models import ClientModel, CoursesModel, CoursesRegisteredModel, TeachingCoursesRegisteredModel
from database.engine import engine
from domain.clients.clients_repository import create_password
from sqlmodel import Session, select



def generate_demo_data():
    with Session(engine) as db:
        # delete all users and courses that aren't root
        query = select(ClientModel).where(ClientModel.account_type != 1)
        results = db.exec(query)

        for result in results:
            db.delete(result)


        db.execute("TRUNCATE `courses`")
        db.execute("TRUNCATE `attendance`")
        db.execute("TRUNCATE `courses_registered`")
        db.execute("TRUNCATE `teaching_courses_registered`")

        # create courses
        courses = [
            CoursesModel(course=11111, course_number="IS 241210", course_title="Systems Analysis and Design",
                         credit_hours=3, capacity=10),
            CoursesModel(course=11112, course_number="IS 141230", course_title="Graphics for the Web",
                         credit_hours=3, capacity=10),
            CoursesModel(course=11113, course_number="MTH 180511", course_title="Introductory Statistics",
                         credit_hours=3, capacity=10),
            CoursesModel(course=11114, course_number="IS 167601", course_title="C++ Programming I",
                         credit_hours=4, capacity=10),
        ]

        for course in courses:
            db.add(course)
        db.commit()

        # create professors
        prof1 = ClientModel(email="prof1@my.stlcc.edu", password=create_password("1234"), firstname="Prof. 1",
                            lastname="Doe", account_type=2)
        prof2 = ClientModel(email="prof2@my.stlcc.edu", password=create_password("1234"), firstname="Prof. 2",
                            lastname="Doe", account_type=2)
        db.add(prof1)
        db.add(prof2)
        db.commit()

        # assign profs to their courses
        db.add(TeachingCoursesRegisteredModel(client_id=prof1.id, course_id=courses[0].id))
        db.add(TeachingCoursesRegisteredModel(client_id=prof1.id, course_id=courses[1].id))
        db.add(TeachingCoursesRegisteredModel(client_id=prof2.id, course_id=courses[2].id))
        db.add(TeachingCoursesRegisteredModel(client_id=prof2.id, course_id=courses[3].id))
        db.commit()

        # create & assign 15 students to each course
        count = 1
        reset = 0
        students = 2
        clients = []
        curr = 0
        while reset <= students:
            client = ClientModel(email="student%d@my.stlcc.edu" % count, password=create_password("abcd"),
                               firstname="Student. %d" % count, lastname="Doe", account_type=3)
            db.add(client)
            clients.append(client)
            count += 1
            curr += 1
            reset += 1
        db.commit()

        curr = 0
        count = 0
        for client in clients:
            course = courses[curr]
            if course is not None:
                db.add(CoursesRegisteredModel(client_id=client.id, course_id=course.id))

            # at the 15's student, go to the next course and assign them to the next class
            if count == 2:
                curr += 1
                count = 0
            count += 1

        db.commit()