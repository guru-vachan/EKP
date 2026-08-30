from pydantic import BaseModel

from pathlib import Path

from app.schemas.metadata import Metadata

class Document(BaseModel):
    document_id: str 
    source: str 
    file_name: str 
    file_path: Path 
    content: str 
    metadata: Metadata