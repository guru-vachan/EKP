from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class Metadata(BaseModel):
    title: str 
    author: str 
    subject: str 
    creator: str 
    producer: str 
    creation_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    page_count: int
    file_size: int 