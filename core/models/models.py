from datetime import datetime

from sqlalchemy import Column, VARCHAR, TIMESTAMP, TEXT

from .base import Base


class Post(Base):
    title: str = Column(VARCHAR(128), nullable=False, unique=True)
    body: str = Column(TEXT, nullable=False)
    date_created: datetime = Column(TIMESTAMP, default=datetime.now())
    slug: str = Column(VARCHAR(150), nullable=False, unique=True)

    def __repr__(self) -> str:
        return self.title

    @property
    def format_date(self) -> str:
        return self.date_created.strftime('%H:%M %d.%m.%Y')
