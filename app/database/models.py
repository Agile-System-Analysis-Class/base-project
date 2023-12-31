### Contributors: Lamonte Harris
### Description: Database models file that represents objects paired to our database

from typing import Optional
from sqlmodel import SQLModel, Field

class ClientModel(SQLModel, table=True):
    """
    Database Client model that represents the IT, Professor & Student Accounts
    """
    __tablename__ = "clients"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    password: str
    firstname: str
    lastname: str
    account_type: int # 1 - root, 2 - professor, 3 - student
    current_time_override: Optional[int] = Field(default=0)

    def to_json(self):
        return {
            "id": self.id,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "name": f"{self.firstname} {self.lastname}",
        }


class CoursesModel(SQLModel, table=True):
    """
    DB Courses model that represents courses for the class
    """
    __tablename__ = "courses"

    id: Optional[int] = Field(default=None, primary_key=True)
    course: int # ##-####
    course_number: str
    course_title: str
    credit_hours: int
    capacity: int
    access_code: Optional[str] = Field(default="")
    start_date: Optional[int] = Field(default=0)
    finish_date: Optional[int] = Field(default=0)
    meeting_start_time: Optional[int] = Field(default=0)


class CoursesRegisteredModel(SQLModel, table=True):
    """
    Db Courses Registered model, connects the professors to which courses they teach
    """
    __tablename__ = "courses_registered"

    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="clients.id")
    course_id: int = Field(foreign_key="courses.id")
    grade: Optional[int] = None
    register_date: Optional[int] = None


class TeachingCoursesRegisteredModel(SQLModel, table=True):
    """
    Db Teach Courses Registered model, connects the professors to which courses they teach
    """
    __tablename__ = "teaching_courses_registered"

    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="clients.id")
    course_id: int = Field(foreign_key="courses.id")
    register_date: Optional[int] = None


class AttendanceModel(SQLModel, table=True):
    """
    Db Attendance Model, keeps track of students attendance for a course
    """
    __tablename__ = "attendance"

    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int
    client_id: int
    date_marked_present: Optional[str] = Field(default="")