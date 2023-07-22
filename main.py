from fastapi import FastAPI, Request, UploadFile, File, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse
from csv_module.router import router as csv_router
from auth.base_config import auth_backend
from auth.manager import get_user_manager
from csv_funcs import get_head
import asyncio
import os
import json
import uuid
from fastapi_users import FastAPIUsers
from pages.router import router as router_account
from auth.models import User
from auth.schemas import UserCreate, UserRead

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # 'RuntimeError: There is no current event loop...'
        loop = None

    if loop and loop.is_running():
        print('Async event loop already running. Adding coroutine to the event loop.')
        tsk = loop.create_task(get_head("csv_files/neo_v2.csv"))
        # ^-- https://docs.python.org/3/library/asyncio-task.html#task-object
        # Optionally, a callback function can be executed when the coroutine completes
        tsk.add_done_callback(
            lambda t: print(f'Task done with result={t.result()}  << return val of get_head()'))
    else:
        print('Starting new event loop')
        result = asyncio.run(get_head("csv_files/neo_v2.csv"))
    """
    # parsed_csv = await get_head("./csv_files/neo_v2.csv")
    # print(parsed_csv)
    # parsed_csv.replace("&lt;", "<")
    # parsed_csv.replace("&gt;", ">")
    return templates.TemplateResponse("base.html", {"request": request})
"""
async def root():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # 'RuntimeError: There is no current event loop...'
        loop = None

    if loop and loop.is_running():
        print('Async event loop already running. Adding coroutine to the event loop.')
        tsk = loop.create_task(get_head("csv_files/neo_v2.csv"))
        # ^-- https://docs.python.org/3/library/asyncio-task.html#task-object
        # Optionally, a callback function can be executed when the coroutine completes
        tsk.add_done_callback(
            lambda t: print(f'Task done with result={t.result().head()}  << return val of get_head()'))
    else:
        print('Starting new event loop')
        result = asyncio.run(get_head("csv_files/neo_v2.csv"))
    return {"message": "Hello World"}
"""


@app.get("/getFiles", response_class=JSONResponse)
async def get_files(request: Request):
    files = os.listdir('./csv_files')
    return sorted(files)


@app.get("/csv/{filename}", response_class=JSONResponse)
async def say_hello(filename: str):
    return await get_head(filename)


@app.post("/upload-file")
def upload_file(file: UploadFile = File(...)):
    if os.path.exists("csv_files"):
        if not file.filename.endswith(".csv"):
            return {"Error": "Not a CSV file"}
        file_name = os.path.join(os.getcwd(), "csv_files", file.filename)
        with open(file_name, "wb+") as f:
            f.write(file.file.read())
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/get/", response_class=JSONResponse)
async def get_file(request: Request, id: int):
    print("You chosen file", sorted(os.listdir('./csv_files'))[int(id)])
    filename = sorted(os.listdir('./csv_files'))[int(id)]
    if not filename.endswith(".csv"):
        return json.dumps({"Error": "You must select CSV file"})
    print(await get_head(filename))
    return [await get_head(filename)]


@app.delete("/get/", response_class=JSONResponse)
async def delete_file(request: Request, id: int):
    print(request)
    file = sorted(os.listdir('./csv_files'))[int(id)]
    file_name = os.path.join(os.getcwd(), "csv_files", file)
    os.remove(file_name)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    router_account
)

app.include_router(
    csv_router
)