from fastapi import APIRouter, Request, Depends, UploadFile, File, status
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy import insert, delete
from csv_funcs import get_head
from utils import templates, get_files
from csv_module.models import file as file_model
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
import os
from csv_module.schemas import FilePage

router = APIRouter(
    prefix='/files',
    tags=['Prefix']
)


@router.get('/')
async def get_files_page(request: Request, files=Depends(get_files)):
    return templates.TemplateResponse("files.html", {'request': request, 'files': enumerate(files)})


@router.post('/upload-file', response_class=RedirectResponse)
async def upload_file(file: UploadFile = File(...), session: AsyncSession = Depends(get_async_session)):
    if os.path.exists("csv_files"):
        if not file.filename.endswith(".csv"):
            return {"Error": "Not a CSV file"}
        file_name = os.path.join(os.getcwd(), "csv_files", file.filename)
        with open(file_name, "wb+") as f:
            f.write(file.file.read())
        stmt = insert(file_model).values(name=file.filename)
        await session.execute(stmt)
        await session.commit()
    return RedirectResponse("/files", status_code=status.HTTP_303_SEE_OTHER)


@router.post('/get-file', response_class=JSONResponse)
async def get_file(file: FilePage):
    # response, pages = await get_head(sorted(os.listdir(os.path.join(os.getcwd(), "csv_files")))[file.file], file.page)
    response, pages = await get_head(file.file, file.page)
    return [response, pages]


@router.delete('/get-file')
async def delete_file(file: FilePage, session: AsyncSession = Depends(get_async_session), files=Depends(get_files)):
    stmt = delete(file_model).where(file_model.c.name == files[file.file])
    await session.execute(stmt)
    await session.commit()
    file_path = os.path.join(os.getcwd(), "csv_files", files[file.file])
    os.remove(file_path)

