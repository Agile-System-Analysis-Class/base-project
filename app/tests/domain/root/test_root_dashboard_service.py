import unittest

from database.models import ClientModel, CoursesModel, CoursesRegisteredModel

from domain.root.root_dashboard_service import (filter_course_by_id, filter_students_by_student_id,
                                                filter_students_by_course_id, filter_course_by_id)


class TestRootDashboardService(unittest.TestCase):
    def test_filter_course_by_id_has_course(self):
        items = [CoursesModel(course=111222, id=2)]
        found = filter_course_by_id(2, items)
        self.assertNotEquals(found, None, "Expected course model to exists")
        self.assertEquals(found.id, 2, "Expected course id to be 2")
        self.assertEquals(found.course, 111222, "Expected course to be 111222")

    def test_filter_students_by_id(self):
        items = [ClientModel(email="example@example.com",id=1), ClientModel(email="example2@example.com", id=2)]
        found = filter_students_by_student_id(1, items)
        found2 = filter_students_by_student_id(2, items)
        self.assertNotEquals(found, None, "Expected course model to exists")
        self.assertEquals(found.id, 1, "Expected client id to be 2")
        self.assertEquals(found2.email, "example2@example.com", "Expected client email to be example@example.com")

    def test_filter_students_by_course_id(self):
        students = [
            ClientModel(email="example@example.com",id=1),
            ClientModel(email="example2@example.com", id=2),
            ClientModel(email="example3@example.com", id=3),
        ]
        course_data = [
            CoursesRegisteredModel(id=1, client_id=1, course_id=2),
            CoursesRegisteredModel(id=2, client_id=2, course_id=3),
            CoursesRegisteredModel(id=3, client_id=3, course_id=3),
        ]
        found = filter_students_by_course_id(2, students, course_data)
        found2 = filter_students_by_course_id(3, students, course_data)
        self.assertEquals(len(found), 1, "Expected students lists to be 1")
        self.assertEquals(len(found2), 2, "Expected students list 2 to be 2")

    def test_filter_course_by_id(self):
        items = [
            CoursesModel(course=111222, id=1),
            CoursesModel(course=111223, id=2),
            CoursesModel(course=111224, id=3),
        ]

        self.assertEquals(filter_course_by_id(0, items), None, "Expected course to not exist")
        self.assertEquals(filter_course_by_id(3, items).course, 111224, "Expected course to be 111224")

    def test_sum(self):
        self.assertEquals(ClientModel(email="prof"), ClientModel(email="prof"), "Expected clients to be the same")
        self.assertEquals(6, 6, "Should be 6")

if __name__ == "__main__":
    unittest.main()