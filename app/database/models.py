from typing import Optional
from sqlmodel import SQLModel, Field

class ClientModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    password: str
    firstname: str
    lastname: str
    account_type: int # 1 - root, 2 - professor, 3 - student

class CoursesModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    course: int # ##-####
    course_number: str
    course_title: str
    credit_hours: int
    capacity: int
    access_code: str
    start_date: int
    finish_date: int
    meeting_start_time: int

class CoursesRegisteredModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int
    course_id: int
    grade: int
    register_date: int

class TeachingCoursesRegisteredModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int
    course_id: int
    register_date: int

class AttendanceModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int
    client_id: int
    date_marked_present: int