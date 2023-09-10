from typing import Union

from fastapi import FastAPI, Request
from starlette.responses import FileResponse, HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()

# Setting up the statis directory to be served
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# templates ob ject
templates = Jinja2Templates(directory="views")

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

fake_data = [
    {"name": "john", "age": 20},
    {"name": "lamonte", "age": 33},
]

@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "data": fake_data})


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
