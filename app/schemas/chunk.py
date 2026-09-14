from pydantic import BaseModel, Field

from app.schemas.metadata import Metadata

class Chunk(BaseModel):
    chunk_id: str 
    document_id: str 
    content: str 
    chunk_index: int
    metadata: Metadata = Field(default_factory=Metadata)
    character_count: int | None = None
    
    """
    why we add character_count ?
    Because:
        Metadata -> describe the document 
    while 
        character_count, chunk_index, token_count and embedding_model -> describe the chunk
    """