from __future__ import annotations

from pydantic import BaseModel, ConfigDict

class IngestionResult(BaseModel):
    """
        Result of a successfully completed ingestion operation.
    """
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        arbitrary_types_allowed=True,
    )
    document_id: str 
    file_name: str

    chunk_created: int
    embedded_created: int

    vector_store: str