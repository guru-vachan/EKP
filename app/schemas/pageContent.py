from pydantic import BaseModel

class PageContent(BaseModel):
    page_number: int
    text: str