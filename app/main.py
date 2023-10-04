from typing import Union, Annotated
from uuid import UUID

from dotenv import dotenv_values
from fastapi import FastAPI, Request, Form, Response, Depends, HTTPException
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import CookieParameters, SessionCookie
from sqlmodel import SQLModel
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from domain.courses.courses_repository import find_professor_courses_by_client_id, find_course, find_course_students_by_id
from domain.root.root_repository import generate_demo_data
from helpers.dashboard_helper import display_root_dashboard, display_professor_dashboard, display_student_dashboard
from domain.clients.clients_repository import create_professor_models, create_student_models, find_by_session, \
    find_account_by_id
from domain.clients.clients_service import get_authenticated_user
from database.helpers import setup_database_data, is_setup_complete
from sessions.auth_session_data import AuthSessionData
from sessions.auth_verifier import AuthVerifier
from sessions.authenticate import Authenticate
from database import engine

# templates ob ject
templates = Jinja2Templates(directory="views")

db_config = dotenv_values('.mysql.env')

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


@app.middleware("http")
async def disable_until_setup(request: Request, call_next):
    if not request.url.path.startswith("/env_setup") and not is_setup_complete():
        return templates.TemplateResponse("setup.html", {"request": request})

    response = await call_next(request)
    return response

# Setup student/teacher dashboards
@app.get("/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
def home_page(request: Request, sess: AuthSessionData = Depends(verifier)):
    if not sess:
        return RedirectResponse("/login")

    account = find_by_session(sess)
    if account is None:
        return templates.TemplateResponse("account_error.html", {
            "request": request, "msg": "Account not found"})

    temp: str
    context = {"request": request}

    match account.account_type:
        case 1:
            temp = "root"
            context = display_root_dashboard(request, account)
        case 2:
            temp = "teacher"
            context = display_professor_dashboard(request, account)
        case 3:
            temp = "student"
            context = display_student_dashboard(request, account)
        case _:
            temp = "student"

    return templates.TemplateResponse(f"dashboard/{temp}.html", context)

@app.get("/generate_data", dependencies=[Depends(cookie)])
def root_generate_data(sess: AuthSessionData = Depends(verifier)):
    if not sess:
        return RedirectResponse("/login")

    account = find_by_session(sess)
    if account is None or account.account_type != 1:
        return {"status": False, "message": "Invalid user account"}

    generate_demo_data()

    return {"status": True, "message": "Website data generated"}


# Setup authentication routes
@app.get("/login", response_class=HTMLResponse, dependencies=[Depends(cookie)])
def login_page(request: Request, session_data: AuthSessionData = Depends(verifier)):
    if session_data:
        return RedirectResponse("/")
    return templates.TemplateResponse("auth/login.html", {"request": request})


@app.post("/login", dependencies=[Depends(cookie)])
async def login_page(
    response: Response,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session_data: AuthSessionData = Depends(verifier)
):
    # check if user is already logged in
    if session_data:
        return {"status": True, "message": "already logged in"}

    account = get_authenticated_user(email, password)
    if account is not None:
        auth = Authenticate(response, session, cookie)
        await auth.session_create(account.id, account.email, account.firstname, account.account_type)
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


@app.get('/teacher/course/{cid}', dependencies=[Depends(cookie)])
async def teacher_course(
    cid: int,
    request: Request,
    sess: AuthSessionData = Depends(verifier)
):
    if not sess:
        return RedirectResponse("/login")

    course = find_course(cid)
    if course is None:
        return RedirectResponse("/login")

    students = find_course_students_by_id(cid)

    return templates.TemplateResponse("teacher/course.html", {
        "request": request,
        "course": course,
        "students": students
    })

@app.get('/teacher/course/{cid}/access_code/{uid}', dependencies=[Depends(cookie)])
async def teacher_access_code(
    cid: int,
    uid: int,
    request: Request,
    sess: AuthSessionData = Depends(verifier)
):
    if not sess:
        return RedirectResponse("/login")

    course = find_course(cid)
    if course is None:
        return RedirectResponse("/login")

    student = find_account_by_id(uid)
    if not student:
        return RedirectResponse(f'/teacher/course/{uid}')

    return templates.TemplateResponse("teacher/generate_access_code.html", {
        "request": request,
        "course": course,
        "student": student
    })


@app.get('/student/course/{cid}', dependencies=[Depends(cookie)])
async def student_course(
    cid: int,
    request: Request,
    sess: AuthSessionData = Depends(verifier)
):
    if not sess:
        return RedirectResponse("/login")

    course = find_course(cid)
    if course is None:
        return RedirectResponse("/login")

    return templates.TemplateResponse("student/course.html", {
        "request": request,
        "course": course,
    })


@app.get('/student/course/{cid}/checkin', dependencies=[Depends(cookie)])
async def student_course_checkin(
    cid: int,
    request: Request,
    sess: AuthSessionData = Depends(verifier)
):
    if not sess:
        return RedirectResponse("/login")

    course = find_course(cid)
    if course is None:
        return RedirectResponse("/login")

    # todo: when we add actual data we need to tell the js when the class started when the page loads

    return templates.TemplateResponse("student/course_checkin.html", {
        "request": request,
        "course": course,
    })

@app.get('/env_setup', response_class=HTMLResponse)
async def db_create(request: Request):
    setup_database_data()
    return templates.TemplateResponse("setup_complete.html", {
        "request": request,
    })

# dummy code below

#
# @app.get("/set_session/{sess}")
# async def set_session(sess: str, response: Response):
#     auth = Authenticate(response, session, cookie)
#     name = await auth.session_create(sess, False)
#
#     return f"created session for {name}"
#
#
# @app.get("/whoami", dependencies=[Depends(cookie)])
# async def whoami(session_data: AuthSessionData = Depends(verifier)):
#     if not session_data:
#         return {'login_status': "not logged in"}
#     else:
#         print(session_data)
#         return {'login_status': "logged in"}
#
#
# @app.get('/delete_session')
# async def del_session(response: Response, session_id: UUID = Depends(cookie)):
#     await session.delete(session_id)
#     cookie.delete_from_response(response)
#     return "deleted session"