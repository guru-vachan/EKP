from pydantic import BaseModel

from pathlib import Path

from app.schemas.metadata import Metadata

class Document(BaseModel):
    document_id: str | None = None
    source: str | None = None
    file_name: str | None = None
    file_path: Path | None = None
    content: str | None = None
    metadata: Metadata