from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

class ContextItem(BaseModel):
    """
        single retrived chunk include in the LLM context.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )
    chunk_id: str = Field(
        description="Associated chunk identifier."
    )
    document_id: str

    content: str 

    rank: int = Field(ge=1)

    score: float

    metadata: dict[str, object] = Field(
        default_factory=dict
    )

class Context(BaseModel):
    """
        FInal context pass to  the LLM layer.
    """
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    items: list[ContextItem]

    text: str

    total_chunks: int = Field(ge=0)

    estimated_tokens: int = Field(ge=0)