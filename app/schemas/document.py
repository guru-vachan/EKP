from pydantic import BaseModel

from app.schemas.metadata import Metadata

class Document(BaseModel):
    document_id: str | None = None
    source: str | None = None
    file_name: str | None = None
    file_path: str | None = None
    content: str | None = None
    metadata: Metadata