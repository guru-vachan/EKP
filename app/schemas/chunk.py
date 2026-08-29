from pydantic import BaseModel

from app.schemas.metadata import Metadata

class Chunk(BaseModel):
    chunk_id: str | None = None
    document_id: str | None = None
    content: str | None = None
    chunk_index: int
    metadata: Metadata
    character_count: int

    """
    why we add character_count ?
    Because:
        Metadata -> describe the document 
    while 
        character_count, chunk_index, token_count and embedding_model -> describe the chunk
    """