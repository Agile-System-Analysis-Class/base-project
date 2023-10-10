### Contributors: Lamonte Harris
### Description: These routes are used to transverse through the website, administrator routes

from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse

from app.database.helpers import setup_database_data
from app.dependencies import  templates

router = APIRouter()

@router.get('/env_setup', response_class=HTMLResponse)
async def db_create(request: Request):
    """
    Sets up the db tables & root account

    :param request:
    :return: Response
    """
    setup_database_data()
    return templates.TemplateResponse("setup_complete.html", {
        "request": request,
    })