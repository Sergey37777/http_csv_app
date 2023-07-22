from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
from utils import templates


router = APIRouter(
    prefix='/account',
    tags=['Pages']
)


@router.get('/')
def get_account_page(request: Request):
    return templates.TemplateResponse("account.html", {'request': request})
