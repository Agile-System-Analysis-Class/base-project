from database.models import ClientModel
from fastapi import Request

def display_root_dashboard(request: Request, acct: ClientModel):
    return {"request": request}