from fastapi.templating import Jinja2Templates
import os


templates = Jinja2Templates(directory="templates")


def get_files():
    files = os.listdir('./csv_files')
    return sorted(files)
