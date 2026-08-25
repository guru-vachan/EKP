from pydantic import BaseModel

from app.schemas.metadata import Metadata

class Chunk(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    chunk_index: int
    metadata: Metadata