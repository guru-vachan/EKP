from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class Metadata(BaseModel):
    title: str | None = None
    author: str | None = None
    subject: str | None = None
    creator: str | None = None
    producer: str | None = None
    creation_date: datetime | None = None
    modified_date: datetime | None = None
    page_count: int = 0
    character_count: int = 0
    word_count: int = 0
    file_size: int = 0
    file_name: str | None = None
    file_extension: str | None = None
    checksum: str | None = None
