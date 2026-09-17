from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

class Citation(BaseModel):

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )
    chunk_id: str = Field(
        description="Associated chunk identifier."
    )
    document_id: str

    citation_id: str

    source: str | None = None

    page_number: int | None = Field(
        default=None,
        gt=0
    )

    rank: int = Field(
        ge=1
    )