from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

class SearchResult(BaseModel):
    """
        Represents a single vector search result.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid" 
    )

    chunk_id: str

    score: float

    rank: int = Field(
        ge=1,
        description="rank in the search results." 
    )

    vector_store: int