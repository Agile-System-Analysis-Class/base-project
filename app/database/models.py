from typing import Optional
from sqlmodel import SQLModel, Field

class ClientModel(SQLModel, table=True):
    __tablename__ = "clients"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    password: str
    firstname: str
    lastname: str
    account_type: int # 1 - root, 2 - professor, 3 - student

class CoursesModel(SQLModel, table=True):
    __tablename__ = "courses"

    id: Optional[int] = Field(default=None, primary_key=True)
    course: int # ##-####
    course_number: str
    course_title: str
    credit_hours: int
    capacity: int
    access_code: Optional[str] = None
    start_date: Optional[int] = None
    finish_date: Optional[int] = None
    meeting_start_time: Optional[int] = None

class CoursesRegisteredModel(SQLModel, table=True):
    __tablename__ = "courses_registered"

    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="clients.id")
    course_id: int = Field(foreign_key="courses.id")
    grade: Optional[int] = None
    register_date: Optional[int] = None

class TeachingCoursesRegisteredModel(SQLModel, table=True):
    __tablename__ = "teaching_courses_registered"

    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="clients.id")
    course_id: int = Field(foreign_key="courses.id")
    register_date: Optional[int] = None

class AttendanceModel(SQLModel, table=True):
    __tablename__ = "attendance"

    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int
    client_id: int
    date_marked_present: Optional[int] = None