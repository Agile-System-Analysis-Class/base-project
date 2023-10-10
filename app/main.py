### Contributors: Lamonte Harris
### Description: This is the main application that creates our student attendance manager demo.
### This file sets up all our pages that allows us to transverse through the entirety of the app

from fastapi import Request, FastAPI
from starlette.staticfiles import StaticFiles

from app.database.helpers import is_setup_complete
from app.dependencies import templates
from app.routers import it_router, auth_router, teacher_router, student_router, dashboard_router

# setup Fast API
app = FastAPI()

# Setting up the statis directory to be served
app.mount("/website/app/assets", StaticFiles(directory="app/assets"), name="assets")


@app.middleware("http")
async def disable_until_setup(request: Request, call_next):
    """
    Route middlewhere to check if we should tell the user if the site is setup or not

    :param request:
    :param call_next:
    :return: Response
    """
    if not request.url.path.startswith("/env_setup") and not is_setup_complete():
        return templates.TemplateResponse("setup.html", {"request": request})

    response = await call_next(request)
    return response

# setup routers
app.include_router(it_router.router)
app.include_router(auth_router.router)
app.include_router(teacher_router.router)
app.include_router(student_router.router)
app.include_router(dashboard_router.router)
