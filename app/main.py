from typing import Union, Annotated
from uuid import UUID

from fastapi import FastAPI, Request, Form, Response, Depends, HTTPException
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import CookieParameters, SessionCookie
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

import services.database
from services.course_helper import filter_courses
from sessions.auth_session_data import AuthSessionData
from sessions.auth_verifier import AuthVerifier
from sessions.authenticate import Authenticate

db = services.database.conn()

# templates ob ject
templates = Jinja2Templates(directory="views")

# setup dummy data
user_data = [
    {"id": 1, "name": "root", "is_student": False},
    {"id": 2, "name": "teacher@my.stlcc.edu", "is_student": False},
    {"id": 3, "name": "student@my.stlcc.edu", "is_student": True},
]

course_data = [
    {"id": 1, "name": "Systems Analysis and Design", "course_id": 241210, "course_code": "is"},
    {"id": 2, "name": "Graphics for the Web", "course_id": 141230, "course_code": "is"},
    {"id": 3, "name": "Introductory Statistics", "course_id": 180511, "course_code": "mth"},
]

teacher_course_data = [
    {"id": 1, "course_id": 1, "teacher_id": 1},
    {"id": 2, "course_id": 2, "teacher_id": 2},
    {"id": 3, "course_id": 3, "teacher_id": 2},
]

student_course_data = [
    {"id": 1, "course_id": 1, "student_id": 3},
    {"id": 2, "course_id": 2, "student_id": 3},
    {"id": 3, "course_id": 3, "student_id": 3},
]

# setup session + backend cookies
cookie_params = CookieParameters()

# Uses UUID
cookie = SessionCookie(
    cookie_name="cookie",
    identifier="auth_verifier",
    auto_error=False,
    secret_key="DONOTUSE", # create unique hash for this eventually
    cookie_params=cookie_params,
)

session = InMemoryBackend[UUID, AuthSessionData]()

verifier = AuthVerifier(
    identifier="auth_verifier",
    auto_error=False,  # off so it doesn't kill our application
    backend=session,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)

# setup Fast API
app = FastAPI()

# Setting up the statis directory to be served
app.mount("/assets", StaticFiles(directory="assets"), name="assets")


# Setup student/teacher dashboards
@app.get("/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
def home_page(request: Request, sess: AuthSessionData = Depends(verifier)):
    if not sess:
        return RedirectResponse("/login")

    temp = "teacher.html"
    courses = teacher_course_data
    course_type = 1
    if sess.is_student:
        temp = "student.html"
        courses = student_course_data
        course_type = 2;

    # grab correct course data for teacher vs student
    cdata = filter_courses(sess.id, courses, course_data, course_type)

    return templates.TemplateResponse(f"dashboard/{temp}", {"request": request, "courses": cdata})


# Setup authentication routes
@app.get("/login", response_class=HTMLResponse, dependencies=[Depends(cookie)])
def login_page(request: Request, session_data: AuthSessionData = Depends(verifier)):
    if session_data:
        return RedirectResponse("/")
    return templates.TemplateResponse("auth/login.html", {"request": request})


@app.post("/login", dependencies=[Depends(cookie)])
async def login_page(
    response: Response,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session_data: AuthSessionData = Depends(verifier)
):
    # check if user is already logged in
    if session_data:
        return {"status": True, "message": "already logged in"}

    # loop through fake data and check if user exists, no PW matching
    for user in user_data:
        if user["name"] == username:
            auth = Authenticate(response, session, cookie)
            await auth.session_create(user["id"], user["name"], user["is_student"])
            return {"status": True, "message": "Logged in successfully!"}
    return {"status": False, "message": "Login failed, please try again!"}


@app.get('/logout', dependencies=[Depends(cookie)])
async def logout(
    response: Response,
    session_id: UUID = Depends(cookie),
    session_data: AuthSessionData = Depends(verifier)
):
    if session_data:
        await session.delete(session_id)
        cookie.delete_from_response(response)
    return RedirectResponse("/login")
# dummy code below


@app.get("/set_session/{sess}")
async def set_session(sess: str, response: Response):
    auth = Authenticate(response, session, cookie)
    name = await auth.session_create(sess, False)

    return f"created session for {name}"


@app.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: AuthSessionData = Depends(verifier)):
    if not session_data:
        return {'login_status': "not logged in"}
    else:
        return {'login_status': "logged in"}


@app.get('/delete_session')
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await session.delete(session_id)
    cookie.delete_from_response(response)
    return "deleted session"


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
