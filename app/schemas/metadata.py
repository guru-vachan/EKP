from datetime import datetime

from pydantic import BaseModel

class Metadata(BaseModel):
    title: str | None = None
    author: str | None = None
    subject: str | None = None
    creator: str | None = None
    producer: str | None = None
    creation_date: datetime | None = None
    modified_date: datetime | None = None
    page_count: int
    file_size: int 