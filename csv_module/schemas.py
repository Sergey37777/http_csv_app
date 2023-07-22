from pydantic import BaseModel


class FilePage(BaseModel):
    file: int
    page: int

