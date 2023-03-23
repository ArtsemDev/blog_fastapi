from datetime import datetime

from pydantic import BaseModel


class PostSchema(BaseModel):
    id: int
    title: str
    body: str
    date_created: datetime

    @property
    def format_date(self) -> str:
        return self.date_created.strftime('%H:%M %d.%m.%Y')

    class Config:
        orm_mode = True
